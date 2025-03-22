import os
import sys
import argparse
import subprocess
from pathlib import Path

from pathlib import Path

# Define project root
project_root = Path(__file__).resolve().parent

parser = argparse.ArgumentParser()
parser.add_argument("--agent", required=True, help="Name of the agent to run (e.g., products)")
args = parser.parse_args()


# Define your agent entrypoints (relative to project root)
agent_entrypoint = {
    "products": "agents/products/products_mcp_stdio_server.py",
    "blog": "agents/blog/blog_mcp_stdio_server.py",
    "recipes": "agents/recipes/recipes_mcp_stdio_server.py"
}

venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

subprocess.Popen(
    [venv_python, str(agent_entrypoint[args.agent])],
    env={"PYTHONPATH": str(project_root), **os.environ}
)


# subprocess.Popen([venv_python, agent_entrypoint], env={"PYTHONPATH": str(project_root), **os.environ})


def set_pythonpath():
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    os.environ['PYTHONPATH'] = project_root
    print(f"✅ PYTHONPATH set to: {project_root}\n")


def run_products_agent():
    from agents.products.product_agent import run_agent
    import asyncio
    print("🧠 Launching Products Agent via STDIO...")
    asyncio.run(run_agent())


def run_blog_agent():
    print("🚧 Blog Agent not yet implemented.")


def run_recipes_agent():
    print("🚧 Recipes Agent not yet implemented.")


def main():
    parser = argparse.ArgumentParser(description="CyberLorian Agent Launcher")
    parser.add_argument("--agent", type=str, help="Choose agent: products | blog | recipes")
    args = parser.parse_args()

    set_pythonpath()

    if args.agent == "products":
        run_products_agent()
    elif args.agent == "blog":
        run_blog_agent()
    elif args.agent == "recipes":
        run_recipes_agent()
    else:
        print("❌ Invalid agent. Use --agent products | blog | recipes")


if __name__ == "__main__":
    main()
