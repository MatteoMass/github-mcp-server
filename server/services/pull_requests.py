from server.utils.github_api import GithubClient
import logging

logger = logging.getLogger(__name__)


class PullRequestService:
    """Read-only pull-request queries."""

    def __init__(self, client: GithubClient):
        self.client = client

    async def get_pr_list(self, owner: str, repo: str, state: str = "open"):
        """
        List pull requests for a repository.

        Args:
            owner (str): Repository owner.
            repo (str):  Repository name.
            state (str): ``open``, ``closed`` or ``all``.

        Returns:
            List of PR dicts.
        """
        params = {"state": state}
        return await self.client.GET(f"{owner}/{repo}/pulls", params=params)


    async def create(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: str | None = None,
        draft: bool = False,
    ):
        """
        Create a pull request (`POST /pulls`).

        Args:
            owner: Repository owner.
            repo:  Repository name.
            title: PR title.
            head:  The branch/tag you want to merge **from** (`user:branch` accepted).
            base:  The branch you want to merge **into** (usually `main`).
            body:  Optional Markdown description.
            draft: Whether to open as a draft PR.

        Returns:
            JSON describing the new pull request.
        """
        payload = {
            "title": title,
            "head": head,
            "base": base,
            "body": body or "",
            "draft": draft,
        }
        return await self.client.POST(f"{owner}/{repo}/pulls", json=payload)