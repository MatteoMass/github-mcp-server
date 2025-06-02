"""
This module contains tools for managing Github Issues
"""

from server.tools import issues


def register_tools(mcp):
    """Register tools with the MCP server."""

    mcp.add_tool(issues.get_issues)
