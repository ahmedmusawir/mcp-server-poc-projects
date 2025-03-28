import os
import sys

# Add the project root to sys.path if it's not already there
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added project root to sys.path: {project_root}")

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
    from dotenv import load_dotenv
    from mcp import StdioServerParameters
    from utils.agent_utils import create_mcp_agent_executor  # NEW - Absolute import

    load_dotenv()

    env = os.environ.copy()
    env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 

    # Path to the venv's Python executable
    venv_python = os.path.join(os.getcwd(), ".venv", "bin", "python")

    server_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")

    server_params = StdioServerParameters(command=venv_python, args=[server_path], env=env)

    async def run_test():
        agent_node = await create_mcp_agent_executor(server_params, create_product_agent)

        # Simulate LangGraph-style input
        input_data = {
            "messages": [{"role": "user", "content": "Show me category list"}]
        }

        # Run the node
        output = await agent_node(input_data)
        print("\n🧪 Product Agent Output:")
        print(output["messages"][-1].content)
        print("-" * 40)

    asyncio.run(run_test())