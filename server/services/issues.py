"""
Service for managing Github issues in MCP server.
"""
from server.utils.github_api import GithubClient

import logging
logger = logging.getLogger(__name__)

class IssueService:
    """
    Service class for managing Github repo
    """

    def __init__(self, client: GithubClient):
        self.client = client

    async def get_issues(self, owner:str, repo: str) -> any:
        """Retrieves a specific issues from repo.

        Args:
            repo (str): The ID of the board to retrieve.
            owner (str): The owner of the repository.

        Returns:
            any: The list of issues.
        """
        response = await self.client.GET(f"{owner}/{repo}/issues")
        return response


