"""
MCP Tools exposing GitHub issue operations.
"""
import logging
from typing import List, Dict, Any
from mcp.server.fastmcp import Context

from server.services.issues import IssueService
from server.github import client

logger = logging.getLogger(__name__)
service = IssueService(client)


# ───────────────────────────────────────────────────────────────────────── #
# READ

async def get_issues(ctx: Context, owner: str, repo: str) -> Dict[str, List[str]]:
    """
    Retrieves issues from repo

    Args:
        ctx:   FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str):  Repository name.

    Returns:
        {"issues": [title, …]}
    """
    try:
        logger.info(f"Getting issues from repo: {repo}")
        issues = await service.get_issues(owner, repo)
        titles = [i["title"] for i in issues if "pull_request" not in i]
        logger.info(f"Successfully retrievedissues: {titles}")
        return {"issues": titles}
    except Exception as exc:
        error_msg = f"Failed to get issues: {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise


# ───────────────────────────────────────────────────────────────────────── #
# WRITE

async def create_issue(
    ctx: Context, owner: str, repo: str, title: str, body: str | None = None
) -> Dict[str, Any]:
    """
    Opens a new issue.

    Args:
        ctx: FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str): Repository name.
        title (str): Issue title.
        body (str): Body of the issue.

    Returns:
        {"url": "...", "number": 123}
    """
    try:
        logger.info(f"Creating an issue in repo: {repo}, with title: {title}")
        result = await service.create_issue(owner, repo, title, body)
        logger.info(f"Successfully created issue number {result['number']}")
        return {"url": result["html_url"], "number": result["number"]}
    except Exception as exc:
        error_msg = f"Failed to create issue {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise


async def comment_issue(
    ctx: Context, owner: str, repo: str, issue_number: int, body: str
) -> Dict[str, str]:
    """
    Adds a comment on an existing issue.

    Args:
        ctx: FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str): Repository name.
        issue_number (int): Issue number.
        body (str): Body of the issue.
    """
    try:
        logger.info(f"Commenting on issue number {issue_number} in repo {repo}")
        result = await service.comment_issue(owner, repo, issue_number, body)
        logger.info(f"Successfully added comment on issue number {issue_number} in repo {repo}")
        return {"url": result["html_url"]}
    except Exception as exc:
        error_msg = f"Failed to add the comment {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise


async def close_issue(
    ctx: Context, owner: str, repo: str, issue_number: int
) -> Dict[str, str]:
    """
    Closes an issue.

    Args:
        ctx: FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str): Repository name.
        issue_number (int): Issue number.

    Returns:
        Dict
    """
    try:
        logger.info(f"Closing issue number {issue_number} in repo {repo}")
        await service.close_issue(owner, repo, issue_number)
        logger.info(f"Successfully closed on issue number {issue_number} in repo {repo}")
        return {"status": "closed"}
    except Exception as exc:
        error_msg = f"Failed to close the issue number {issue_number} in repo {repo}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise
