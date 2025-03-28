# agents/products/product_agent_module.py
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent


async def create_product_agent(session):
    """
    Creates a ReAct-style product agent using LangChain and MCP tools.
    This function is meant to be used in orchestrated LangGraph workflows.

    Args:
        session: MCP ClientSession instance with an active connection.

    Returns:
        A LangChain ReAct agent ready to handle product-related queries.
    """
    tools = await load_mcp_tools(session)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
    return create_react_agent(llm, tools)


# Optional test entry point to validate this agent independently
if __name__ == "__main__":
    import asyncio
    import os
    import sys
    from dotenv import load_dotenv
    from mcp import StdioServerParameters
    from utils.agent_utils import create_mcp_agent_executor  

    load_dotenv()

    server_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")

    server_params = StdioServerParameters(command=sys.executable, args=[server_path])

    async def run_test():
        agent_node = await create_mcp_agent_executor(server_params, create_product_agent)

        # Simulate LangGraph-style input
        input_data = {
            "messages": [{"role": "user", "content": "Show me category list"}]
        }

        # Run the node
        output = await agent_node(input_data)
        print("\n Product Agent Output:")
        print(output["messages"][-1].content)
        print("-" * 40)

    asyncio.run(run_test())