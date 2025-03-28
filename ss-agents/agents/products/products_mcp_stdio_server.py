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
    try:
        print("Fetching products...")
        data = list_products()
        print("Fetched products")
        return data
    except Exception as e:
        print("Tool failed:", e)
        return {"error": str(e)}


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
