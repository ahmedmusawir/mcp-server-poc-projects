# from mcp import tool
# from mcp.types import tool
import requests

API_BASE_URL = "https://dummyjson.com/products"

# @tool()
def list_products() -> dict:
    """Fetch the default list of products (30 items)"""
    response = requests.get(f"{API_BASE_URL}?limit=30")
    return response.json()

# @tool()
def search_product_by_word(query: str) -> dict:
    """Search for products by keyword"""
    response = requests.get(f"{API_BASE_URL}/search?q={query}")
    return response.json()

# @tool()
def list_categories() -> dict:
    """List all product categories available"""
    response = requests.get(f"{API_BASE_URL}/categories")
    return response.json()

# @tool()
def get_products_by_category(category: str) -> dict:
    """List products within a specific category"""
    response = requests.get(f"{API_BASE_URL}/category/{category}")
    return response.json()
