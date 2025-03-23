from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

env = os.environ.copy()
env["PYTHONPATH"] = os.getcwd()
env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Path to the venv's Python executable
venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

# Path to the MCP server script
server_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")
server_params = StdioServerParameters(command=venv_python, args=[server_path], env=env)


# --- Product Agent (MCP-backed) ---
async def create_product_agent(session):
    tools = await load_mcp_tools(session)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
    return create_react_agent(llm, tools)

# --- Weather Agent (for demonstration) ---
# (Your existing weather_agent function, unchanged)
def weather_agent(city: str):
    """
    Creates a modular weather agent with its own toolset.
    Returns the weather_agent for integration into the graph.
    """
    # Define the LLM
    llm = ChatOpenAI(model_name='gpt-4o', temperature=0.5)

    # Define the weather tool
    @tool
    def get_weather(city: str):
        """Call to get the current weather. Use this anytime asked about the weather."""
        if city.lower() == "paris":
            return "It's always sunny in Paris."
        else:
            return "It's cold and wet."

    # Create the weather agent
    weather_agent_instance = create_react_agent(llm, tools=[get_weather])
    return weather_agent_instance


# --- LangGraph Setup ---

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the graph builder
graph_builder = StateGraph(State)

# Define the LLM for the prompt_nexus
llm = ChatOpenAI(model_name='gpt-4o', temperature=0.5)

# Define the prompt_nexus node
def prompt_nexus(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add the prompt_nexus node to the graph
graph_builder.add_node("prompt_nexus", prompt_nexus)

# --- Node for the Product Agent (with connection management) ---
async def product_agent_node(state: State):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = await create_product_agent(session)  # Create the agent
            response = await agent.ainvoke(state) # Pass entire state
            return response # Return the agent's full response
            # connection is closed when exiting the 'async with' blocks

# Add the product agent node
graph_builder.add_node("products_agent", product_agent_node)

# --- Add Weather Agent Node (for comparison/demonstration) ---

async def weather_agent_node(state: State):
  agent = weather_agent("") #dummy arg
  response = await agent.ainvoke(state)
  return response

graph_builder.add_node("weather_agent", weather_agent_node)


# --- Routing Logic ---

def route_to_agent(state: State):
    last_message = state["messages"][-1].content.lower()
    if "weather" in last_message:
        return "weather_agent"
    elif "product" in last_message or "buy" in last_message:
        return "products_agent"
    return END  # Or route to a default node

# Add conditional edges
graph_builder.add_conditional_edges("prompt_nexus", route_to_agent, {
    "weather_agent": "weather_agent",
    "products_agent": "products_agent",
    END: END
})

# Add normal edges
graph_builder.add_edge("weather_agent", END)
graph_builder.add_edge("products_agent", END)

# Set entry point
graph_builder.set_entry_point("prompt_nexus")

# Compile the graph
graph = graph_builder.compile()

# --- Run the Graph ---

async def main():
    # Test the graph with different inputs
    inputs = [
        {"messages": [{"role": "user", "content": "What's the weather like?"}]},
        {"messages": [{"role": "user", "content": "Show me some products."}]},
        {"messages": [{"role": "user", "content": "Can I buy a phone?"}]},
        {"messages": [{"role": "user", "content": "What is two plus two?"}]}, # Example of a question neither agent handles
    ]

    for input_data in inputs:
        result = await graph.ainvoke(input_data)
        print(f"Input: {input_data['messages'][-1]['content']}")
        print(f"Output: {result['messages'][-1].content}")  # Print the last message
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(main())