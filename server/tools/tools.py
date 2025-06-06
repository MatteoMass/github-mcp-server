"""
This module contains tools for managing Github Issues
"""

from server.tools import issues, pull_requests, repo, repo_to_text,branches, contents


def register_tools(mcp):
    """Register tools with the MCP server."""

    # ISSUES
    mcp.add_tool(issues.get_issues)
    mcp.add_tool(issues.create_issue)
    mcp.add_tool(issues.comment_issue)
    mcp.add_tool(issues.close_issue)

    # PULL REQUESTS
    mcp.add_tool(pull_requests.get_pull_requests)
    mcp.add_tool(pull_requests.create_pull_request)

    # REPOSITORY
    mcp.add_tool(repo.get_repo_stats)

    # BRANCHES & COMMITS
    mcp.add_tool(branches.list_branches)
    mcp.add_tool(contents.get_recent_commits)
    mcp.add_tool(contents.get_file_contents)

    

    mcp.add_tool(repo_to_text.get_repo_to_text)
