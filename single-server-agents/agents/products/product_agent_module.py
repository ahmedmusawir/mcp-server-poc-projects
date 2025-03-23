from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import sys
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

# Async function to return a fully initialized ReAct agent with product tools
async def get_product_agent():
    server_params = StdioServerParameters(command=venv_python, args=[server_path], env=env)

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            llm = ChatOpenAI(model="gpt-4o", temperature=0.5)
            return create_react_agent(llm, tools)

# Standalone test using __main__
if __name__ == "__main__":
    async def run_test():
        agent = await get_product_agent()
        response = await agent.ainvoke({
            # "messages": [{"role": "user", "content": "can you search for phone?"}]
            "messages": [{"role": "user", "content": "show me some products"}]
        })
        print("\n\U0001f6cd\ufe0f Products Response:")
        print(response["messages"][-1].content)

    asyncio.run(run_test())
