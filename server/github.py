import logging
import os

from dotenv import load_dotenv

from server.utils.github_api import GithubClient

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# Initialize Github client and service
try:
    api_key = os.getenv("GITHUB_API_KEY")

    if not api_key:
        raise ValueError(
            "GITHUB_API_KEY must be set in environment variables"
        )
    client = GithubClient(api_key=api_key)
    logger.info("Github client and service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Github client: {str(e)}")
    raise


# Add a prompt for common Github operations
def github_help() -> str:
    """Provides help information about available Github operations."""
    return """
    Available Github Operations:
    1. get issues
    """
