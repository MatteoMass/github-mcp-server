from server.utils.github_api import GithubClient


class RepoService:
    """General repository information."""

    def __init__(self, client: GithubClient):
        self.client = client

    async def get_stats(self, owner: str, repo: str):
        """
        Fetch high-level repo metadata (stars, forks, etc.).

        Args:
            owner (str): Repository owner.
            repo (str):  Repository name.

        Returns:
            JSON with the repository resource.
        """
        return await self.client.GET(f"{owner}/{repo}")