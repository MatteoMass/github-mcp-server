"""
Branch listing tool.
"""
from typing import List, Dict
from mcp.server.fastmcp import Context
from server.services.branches import BranchService
from server.github import client
import logging

logger = logging.getLogger(__name__)
service = BranchService(client)


async def list_branches(ctx: Context, owner: str, repo: str) -> Dict[str, List[str]]:
    """
    Gets the list of branches.

    Args:
        ctx:   FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str):  Repository name.

    Returns:
        {"branches": ["main", "dev", …]}
    """
    try:
        logger.info(f"Getting the list of branches for repository {repo}")
        branches = await service.list_branches(owner, repo)
        names = [b["name"] for b in branches]
        logger.info(f"Successfully getting the list of branches for repository {repo}")
        return {"branches": names}
    except Exception as exc:
        error_msg = f"Error while getting the list of branches for repository {repo}. Error: {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise