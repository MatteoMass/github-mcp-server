from server.utils.github_api import GithubClient


class BranchService:
    """Branch enumeration service."""

    def __init__(self, client: GithubClient):
        self.client = client

    async def list_branches(self, owner: str, repo: str):
        """
        Return branch objects for a repository.

        Args:
            owner (str): Repository owner.
            repo (str):  Repository name.

        Returns:
            List of branch dicts (each containing ``name`` and ``commit`` keys).
        """
        return await self.client.GET(f"{owner}/{repo}/branches")