"""
Repository-level stats tool.
"""
from mcp.server.fastmcp import Context
from server.services.repo import RepoService
from server.github import client
import logging

logger = logging.getLogger(__name__)

service = RepoService(client)


async def get_repo_stats(ctx: Context, owner: str, repo: str):
    """
    Gets the statistics of the repository

    Args:
        ctx:   FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str):  Repository name.

    Returns:
        {"stars": 0, "forks": 0, "watchers": 0, "open_issues": 0}
    """
    try:
        logger.info(f"Getting the statistics for repository {repo}")
        data = await service.get_stats(owner, repo)
        logger.info(f"Successfully retrieving the statistics for repository {repo}")
        return {
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "watchers": data["watchers_count"],
            "open_issues": data["open_issues_count"],
        }
    except Exception as exc:
        error_msg = f"Failed to get statistics of repository {repo}. Error: {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise