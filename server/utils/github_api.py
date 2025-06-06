import logging
import httpx
from server.utils.repo_to_text_utils import fetch_file_contents, fetch_repo_sha, fetch_repo_tree, format_repo_contents, parse_repo_url

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
        return await self._request("get", endpoint, params=params)

    async def POST(self, endpoint: str, json: dict):
        return await self._request("post", endpoint, json=json)

    async def PATCH(self, endpoint: str, json: dict):
        return await self._request("patch", endpoint, json=json)

    async def PUT(self, endpoint: str, json: dict = None):
        return await self._request("put", endpoint, json=json)

    async def _request(self, method: str, endpoint: str, **kwargs):
        headers = self._get_headers()

        try:
            response = await self.client.request(method, endpoint, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during {method.upper()} {endpoint}: {e}")
            raise httpx.HTTPStatusError(
                f"Failed to {method.upper()} {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error during {method.upper()} {endpoint}: {e}")
            raise httpx.RequestError(f"Failed to {method.upper()} {endpoint}: {str(e)}")

    def _get_headers(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.api_key}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    
    async def REPO_TO_TEXT(self, repo_url: str):
        owner, repo, ref, path = parse_repo_url(repo_url)
        sha = fetch_repo_sha(owner, repo, ref, path, self.api_key)
        tree = fetch_repo_tree(owner, repo, sha, self.api_key)
        blobs = [item for item in tree if item['type'] == 'blob']
        common_exts = ('.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.html', '.css')
        selected_files = [item for item in blobs if item['path'].lower().endswith(common_exts)]
        for item in selected_files:
            item['url'] = f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}?ref={ref}" if ref else f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}"
        contents = fetch_file_contents(selected_files,self. api_key)
        return format_repo_contents(contents)
