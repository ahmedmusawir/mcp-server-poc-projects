
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage  # Import message types
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, List, Union
import os
# Import the agent creation function and the factory
from agents.products.product_agent_module import create_product_agent
from utils.agent_utils import create_mcp_agent_executor  # Correct absolute import


async def create_controller_graph(server_params):
    class State(TypedDict):
        messages: Annotated[List[Union[AIMessage, HumanMessage]], add_messages] # type: ignore

    graph_builder = StateGraph(State)

    llm = ChatOpenAI(model_name='gpt-4o', temperature=0.5)

    def prompt_nexus(state: State):
        return {"messages": [llm.invoke(state["messages"])]}

    graph_builder.add_node("prompt_nexus", prompt_nexus)

    # Create the agent executor using the factory
    product_agent_executor = await create_mcp_agent_executor(
        server_params, create_product_agent
    )
    graph_builder.add_node("products_agent", product_agent_executor)

    def route_to_agent(state: State):
        last_message = state["messages"][-1].content.lower()
        if "product" in last_message or "buy" in last_message:
            return "products_agent"
        return END

    graph_builder.add_conditional_edges(
        "prompt_nexus",
        route_to_agent,
        {"products_agent": "products_agent", END: END},
    )

    graph_builder.add_edge("products_agent", END)
    graph_builder.set_entry_point("prompt_nexus")
    return graph_builder.compile()

if __name__ == "__main__":
    import asyncio
    import os
    from dotenv import load_dotenv
    from mcp import StdioServerParameters

    load_dotenv()

    env = os.environ.copy()
    # env["PYTHONPATH"] = os.getcwd()  # No, set it when running
    env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
    server_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")

    server_params = StdioServerParameters(command=venv_python, args=[server_path], env=env)

    async def run_test():
        graph = await create_controller_graph(server_params)

        test_inputs = [
            {"messages": [{"role": "user", "content": "Show me some products"}]},
            {"messages": [{"role": "user", "content": "Can I buy a laptop?"}]},
            {"messages": [{"role": "user", "content": "Just say hello"}]}
        ]

        for input_data in test_inputs:
            response = await graph.ainvoke(input_data)
            print(f"User: {input_data['messages'][-1]['content']}")
            print(f"Agent: {response['messages'][-1].content}")  # Use .content
            print('-' * 40)

    asyncio.run(run_test())