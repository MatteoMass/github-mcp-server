"""
Service for managing GitHub issues in the MCP server.
"""
from server.utils.github_api import GithubClient
import logging

logger = logging.getLogger(__name__)


class IssueService:
    """Business-logic layer for issue operations."""

    def __init__(self, client: GithubClient):
        self.client = client

    # ────────────────────────────────────────────────────────────────── #
    # READ
    async def get_issues(self, owner: str, repo: str) -> any:
        """
        Return every open-issue JSON object for ``owner/repo``.

        Args:
            owner (str): Repository owner/organisation.
            repo (str):  Repository name.

        Returns:
            any: List of issue dicts exactly as returned by the GitHub REST API.
        """
        return await self.client.GET(f"{owner}/{repo}/issues")

    # ────────────────────────────────────────────────────────────────── #
    # WRITE
    async def create_issue(
        self, owner: str, repo: str, title: str, body: str | None = None
    ):
        """
        Create a new issue.

        Args:
            owner (str): Repository owner.
            repo (str):  Repository name.
            title (str): Issue title.
            body (str):  Optional Markdown body.

        Returns:
            JSON payload describing the created issue.
        """
        payload = {"title": title, "body": body or ""}
        return await self.client.POST(f"{owner}/{repo}/issues", json=payload)

    async def comment_issue(
        self, owner: str, repo: str, issue_number: int, body: str
    ):
        """
        Add a comment to an existing issue.

        Args:
            owner (str):         Repository owner.
            repo (str):          Repository name.
            issue_number (int):  Target issue number.
            body (str):          Comment body (Markdown).

        Returns:
            JSON with the new comment metadata.
        """
        payload = {"body": body}
        return await self.client.POST(
            f"{owner}/{repo}/issues/{issue_number}/comments", json=payload
        )

    async def close_issue(self, owner: str, repo: str, issue_number: int):
        """
        Close an issue by setting its state to ``closed``.

        Args:
            owner (str):        Repository owner.
            repo (str):         Repository name.
            issue_number (int): Issue to close.

        Returns:
            JSON for the updated issue.
        """
        payload = {"state": "closed"}
        return await self.client.PATCH(
            f"{owner}/{repo}/issues/{issue_number}", json=payload
        )


