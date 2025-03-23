# Navigate to project root (one folder up from /scripts)
Set-Location -Path (Join-Path $PSScriptRoot "..")

# Set PYTHONPATH to current (now root) directory
$env:PYTHONPATH = (Get-Location).Path

# Run the MCP server
python agents/products/products_mcp_stdio_server.py
