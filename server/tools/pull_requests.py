"""
Pull-request utilities (read-only).
"""
from typing import List, Dict
from mcp.server.fastmcp import Context
from server.services.pull_requests import PullRequestService
from server.github import client
import logging

logger = logging.getLogger(__name__)
service = PullRequestService(client)


async def get_pull_requests(
    ctx: Context, owner: str, repo: str, state: str = "open"
) -> Dict[str, List[str]]:
    """
    Gets the pull requests

    Args:
        ctx:   FastMCP request context (handles errors).
        owner (str): Repository owner.
        repo (str):  Repository name.
        state (str): State of the pull request

    Returns:
        {"pull_requests": ["#1 - Add feature (open)", …]}
    """
    try:
        logger.info(f"Getting the pull requests in {repo}")
        pulls = await service.get_pr_list(owner, repo, state)
        titles = [f"#{pr['number']} - {pr['title']} ({pr['state']})" for pr in pulls]
        logger.info(f"Successfully retrieved the list of pull requests from {repo}")
        return {"pull_requests": titles}
    except Exception as exc:
        error_msg = f"Failed to get pull requests. Error: {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise


async def create_pull_request(
    ctx: Context,
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str,
    body: str | None = None,
    draft: bool = False,
) -> Dict[str, str]:
    """
    Create a pull request.

    Args:
        owner: Repository owner.
        repo:  Repository name.
        title: PR title.
        head:  The branch/tag you want to merge **from** (`user:branch` accepted).
        base:  The branch you want to merge **into** (usually `main`).
        body:  Optional Markdown description.
        draft: Whether to open as a draft PR.

    Returns:
        {"url": pull_request_url, "number": pr_number}
    """
    try:
        logger.info(f"Create a pull requests titled {title} in repository {repo}, branch: {base}")
        pr = await service.create(owner, repo, title, head, base, body, draft)
        logger.info(f"Successfully created the pull requests")
        return {"url": pr["html_url"], "number": pr["number"]}
    except Exception as exc:
        error_msg = f"Error creating the pull request. Error {str(exc)}"
        logger.error(error_msg)
        await ctx.error(str(exc))
        raise