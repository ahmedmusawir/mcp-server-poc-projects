#!/bin/bash

# Get the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to the project root (one level up from the script's directory)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT" || exit 1 # Go to project root, exit script if cd fails

echo "Ensuring Python virtual environment is active..."
# Activate the virtual environment - IMPORTANT!
# Assumes the .venv is in the PROJECT_ROOT
source .venv/bin/activate

echo "Running MCP server (products_mcp_stdio_server.py) from: $(pwd)"
# Run the Python script using its path relative to the project root
python agents/products/products_mcp_stdio_server.py

echo "MCP server script finished."