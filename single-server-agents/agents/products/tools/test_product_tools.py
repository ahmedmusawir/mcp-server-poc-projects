# tests/test_products_tools.py

import os
import sys

tools_dir = os.path.abspath(os.path.join(os.path.dirname(__file__))) #<--- change here.
sys.path.append(tools_dir)
print(f"Added to sys.path: {tools_dir}")

from product_tools import (
    list_products,
    search_product_by_word,
    list_categories,
    get_products_by_category,
)

# This test will check if the API returns the default 30 or limited products.
def test_list_products():
    response = list_products()
    assert "products" in response
    assert isinstance(response["products"], list)
    assert len(response["products"]) > 0

# This test will verify that a search query returns expected results.
def test_search_product_by_word():
    response = search_product_by_word("phone")
    assert "products" in response
    assert isinstance(response["products"], list)
    assert any("phone" in product["title"].lower() for product in response["products"])

# This test checks the categories endpoint.
def test_list_categories():
    response = list_categories()
    assert isinstance(response, list)
    # assert "smartphones" in response
    assert any(item["slug"] == "smartphones" for item in response)


# This test checks if filtering products by category works.
def test_get_products_by_category():
    response = get_products_by_category("smartphones")
    assert "products" in response
    assert isinstance(response["products"], list)
    assert all(product["category"] == "smartphones" for product in response["products"])
