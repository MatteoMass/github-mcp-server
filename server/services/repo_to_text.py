"""
Service for managing Github issues in MCP server.
"""
from server.utils.github_api import GithubClient

import logging
logger = logging.getLogger(__name__)

class RepoToTextService:
    """
    Service class for managing Github repo
    """

    def __init__(self, client: GithubClient):
        self.client = client

    async def get_repo_to_text(self, repo: str) -> any:
        """Retrieves the repo and file structure as text.

        Args:
            owner (str): The owner of the repository.

        Returns:
            any: The list of issues.
        """
        response = await self.client.REPO_TO_TEXT(repo)
        return response
