# github_api.py
import logging

import httpx

# Configure logging
logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com/repos"


class GithubClient:
    """
    Client class for interacting with the Github API over REST.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = GITHUB_API_BASE
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        await self.client.aclose()

    async def GET(self, endpoint: str, params: dict = None):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.api_key}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        try:
            response = await self.client.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to get {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise httpx.RequestError(f"Failed to get {endpoint}: {str(e)}")

