"""
This module contains tools for managing Github.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.services.issues import IssueService
from server.github import client

logger = logging.getLogger(__name__)

service = IssueService(client)


async def get_issues(ctx: Context, owner: str, repo:str) ->List[str]:
    """Retrieves a specific issues from repo.

    Args:
        repo (str): The ID of the board to retrieve.
        owner (str): The owner of the repository.

    Returns:
        List[str]: The list of issues.
    """
    try:
        logger.info(f"Getting issues from repo: {repo}")
        result = await service.get_issues(owner, repo)
        issues_only = [issue["title"] for issue in result if "pull_request" not in issue]
        logger.info(f"Successfully retrieved isses: {issues_only}")
        return {"issues": issues_only}
    except Exception as e:
        error_msg = f"Failed to get board: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise
