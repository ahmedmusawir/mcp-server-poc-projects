import os
import sys

tools_dir = os.path.abspath(os.path.join(os.path.dirname(__file__))) #<--- change here.
sys.path.append(tools_dir)
print(f"Added to sys.path: {tools_dir}")

from mcp.server.fastmcp import FastMCP
from agents.products.tools.product_tools import (
    list_products,
    search_product_by_word,
    list_categories,
    get_products_by_category,
)

# Initialize MCP Server for Products
mcp = FastMCP("Products")

# Register tools with MCP (wrap tested logic)
@mcp.tool()
def list_products_tool() -> dict:
    return list_products()

@mcp.tool()
def search_product_by_word_tool(q: str) -> dict:
    return search_product_by_word(q)

@mcp.tool()
def list_categories_tool() -> list:
    return list_categories()

@mcp.tool()
def get_products_by_category_tool(category: str) -> dict:
    return get_products_by_category(category)

if __name__ == "__main__":
    print("=" * 40)
    print("Starting MCP Server: Product Tools")
    print("Transport Mode: STDIO")
    print("=" * 40)
    mcp.run(transport="stdio")
