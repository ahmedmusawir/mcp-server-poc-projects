import asyncio
import os
from dotenv import load_dotenv
from langgraph.mission_controller import create_controller_graph
from mcp import StdioServerParameters

async def main():
    load_dotenv()
    
    # Set env and paths
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
    server_path = os.path.join(os.getcwd(), "agents", "products", "products_mcp_stdio_server.py")
   
    server_params = StdioServerParameters(command=venv_python, args=[server_path], env=env)

    graph = await create_controller_graph(server_params)

    print("Welcome to the LangGraph chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        messages = [{"role": "user", "content": user_input}]
        response = await graph.ainvoke({"messages": messages})
        print(f"Bot: {response['messages'][-1]['content']}") # Access 'content' directly


if __name__ == "__main__":
    asyncio.run(main())