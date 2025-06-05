"""
Commit and file-content tools.
"""
import base64
from typing import List, Dict
from mcp.server.fastmcp import Context
from server.services.contents import ContentService
from server.github import client
import logging

logger = logging.getLogger(__name__)
service = ContentService(client)


async def get_recent_commits(
    ctx: Context, owner: str, repo: str, branch: str, per_page: int = 10
) -> Dict[str, List[str]]:
    """
    Retrieves the most recent commits.

    Args:
        ctx:   FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str):  Repository name.
        branch (str): Name of the branch
        per_page (int): Max commits to return

    Returns:
        {"commits": ["abc123", …]}
    """
    try:
        logger.info(f"Getting the commits for branch {branch} in {repo}")
        commits = await service.recent_commits(owner, repo, branch, per_page)
        shas = [c["sha"] for c in commits]
        logger.info(f"Successful got the commits for branch {branch} in {repo}")
        return {"commits": shas}
    except Exception as exc:
        error_msg = f"Error while getting the commits for branch {branch} in {repo}. Error {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise


async def get_file_contents(
    ctx: Context, owner: str, repo: str, path: str, ref: str | None = None
) -> Dict[str, str]:
    """
    Retrieves the most recent commits.

    Args:
        ctx:   FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str):  Repository name.
        path (str): File path within the repo
        ref (int): Optional commit SHA / branch / tag.

    Returns:
        {"path": "...", "content": "..."}
    """
    try:
        logger.info(f"Getting the content of file {path} in repository {repo}")        
        blob = await service.get_file(owner, repo, path, ref)
        content = base64.b64decode(blob["content"]).decode()
        logger.info(f"Successfully got the content of file {path} in repository {repo}")        
        return {"path": path, "content": content}
    except Exception as exc:
        error_msg = f"Error while getting the content of file {path} in repository {repo}. Error: {error_msg}"      
        logger.error(error_msg)        
        await ctx.error(str(exc))
        raise