from server.utils.github_api import GithubClient


class ContentService:
    """Commits and file-content helpers."""

    def __init__(self, client: GithubClient):
        self.client = client

    async def recent_commits(
        self, owner: str, repo: str, branch: str, per_page: int = 10
    ):
        """
        Retrieve the most recent commits on a branch.

        Args:
            owner (str):    Repository owner.
            repo (str):     Repository name.
            branch (str):   Branch ref (e.g. ``main``).
            per_page (int): Max commits to return (<=100).

        Returns:
            List of commit dicts.
        """
        params = {"sha": branch, "per_page": per_page}
        return await self.client.GET(f"{owner}/{repo}/commits", params=params)

    async def get_file(
        self, owner: str, repo: str, path: str, ref: str | None = None
    ):
        """
        Download a file’s blob (Base64) from a repo.

        Args:
            owner (str): Repository owner.
            repo (str):  Repository name.
            path (str):  File path within the repo.
            ref (str):   Optional commit SHA / branch / tag.

        Returns:
            GitHub ``contents`` API response including ``content``.
        """
        params = {"ref": ref} if ref else None
        return await self.client.GET(f"{owner}/{repo}/contents/{path}", params=params)