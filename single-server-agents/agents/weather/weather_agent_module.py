from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import os

from dotenv import load_dotenv

load_dotenv()

env = os.environ.copy()
env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# --- Weather Agent (for demonstration) ---
def get_weather_agent(city: str):
    """
    Creates a modular weather agent with its own toolset.
    Returns the weather_agent for integration into the graph.
    """
    # Define the LLM
    llm = ChatOpenAI(model_name='gpt-4o', temperature=0.5)

    # Define the weather tool
    @tool
    def get_weather(city: str):
        """Call to get the current weather. Use this anytime asked about the weather."""
        if city.lower() == "paris":
            return "It's always sunny in Paris."
        else:
            return "It's cold and wet."

    # Create the weather agent
    weather_agent = create_react_agent(llm, tools=[get_weather])
    return weather_agent