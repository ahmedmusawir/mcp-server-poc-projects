from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

env = os.environ.copy()
env["PYTHONPATH"] = os.getcwd()

# Load environment variables
load_dotenv()

model = ChatOpenAI(model="gpt-4o")

# Use the venv's python to launch the MCP server
venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

mcp_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")

server_params = StdioServerParameters(
    command=venv_python,
    args=[mcp_path],
    env=env
    # args=[os.path.join("agents", "products", "products_mcp_stdio_server.py")]
    # args=["/agents/products/products_mcp_stdio_server.py"]
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)

            # Ask it to show the product list
            response = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": "Show me some products."}
                ]
            })

            print("\n🛍️ Products Response:")
            print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(run_agent())
