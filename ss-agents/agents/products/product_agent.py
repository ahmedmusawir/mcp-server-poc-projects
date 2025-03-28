import asyncio
import os
import sys

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

# Load environment variables from .env (optional)
load_dotenv()

# Use whichever model you like
model = ChatOpenAI(model="gpt-4o")

# Path to your server script (relative to top-level folder)
mcp_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")

# Use sys.executable to match the current Poetry environment's python
server_params = StdioServerParameters(
    command=sys.executable,
    args=[mcp_path],
    env=os.environ.copy()  # optional if you want to pass your entire env
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Load the Tools from that server
            tools = await load_mcp_tools(session)

            # Create an agent that can call those Tools
            agent = create_react_agent(model, tools)

            # Example prompt
            response = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": "Show me some products."}
                ]
            })

            print("\nProducts Response:")
            print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(run_agent())
