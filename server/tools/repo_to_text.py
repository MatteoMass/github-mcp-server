"""
This module contains tools for managing Github.
"""

import logging

from server.services.repo_to_text import RepoToTextService
from server.github import client

from mcp.server.fastmcp import Context

logger = logging.getLogger(__name__)

service = RepoToTextService(client)

async def get_repo_to_text(ctx: Context, repo: str) -> str:
    """Retrieves the content of a repository as text.

    Args:
        repo (str): The name of the repository.

    Returns:
        str: The content of the repository as text.
    """
    try:
        logger.info(f"Getting content from repo: {repo}")
        content = await service.get_repo_to_text(repo)
        logger.info(f"Successfully retrieved content from repo: {repo}")
        return content
    except Exception as e:
        error_msg = f"Failed to get content from repo: {str(e)}"
        logger.error(error_msg)
        await ctx.error(error_msg)
        raise