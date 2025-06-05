"""
This module contains tools for managing Github Issues
"""

from server.tools import issues
from server.tools import repo_to_text

def register_tools(mcp):
    """Register tools with the MCP server."""

    mcp.add_tool(issues.get_issues)

    mcp.add_tool(repo_to_text.get_repo_to_text)
