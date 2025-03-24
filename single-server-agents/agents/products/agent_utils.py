# langgraph/agent_utils.py
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def create_mcp_agent_executor(server_params, create_agent_func):
    """
    Creates a LangGraph node function that manages the MCP connection
    and executes the given agent.

    Args:
        server_params: StdioServerParameters for the MCP server.
        create_agent_func: A function that takes a ClientSession and
                          returns an agent instance.

    Returns:
        An asynchronous function suitable for use as a LangGraph node.
    """
    async def agent_node(state):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                agent = await create_agent_func(session)
                response = await agent.ainvoke(state)
                return response
    return agent_node