import os
import sys
import asyncio
from dotenv import load_dotenv
from mcp import StdioServerParameters
from langgraph.mission_controller import create_controller_graph

async def main():
    load_dotenv()
    
    server_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")
   
    server_params = StdioServerParameters(command=sys.executable, args=[server_path])

    graph = await create_controller_graph(server_params)

    print("Welcome to the LangGraph chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        messages = [{"role": "user", "content": user_input}]
        response = await graph.ainvoke({"messages": messages})
        print(f"Bot: {response['messages'][-1].content}") # Access 'content' directly


if __name__ == "__main__":
    asyncio.run(main())