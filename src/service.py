from typing import Any
import httpx
import argparse
from . import JIRA_API_BASE


async def make_request(url: str, method: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, timeout=90.0)
            
            response.raise_for_status()
            
            return response.json()
        except httpx.HTTPStatusError:
            return None
        except httpx.RequestError:
            return None
        except Exception:
            return None

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="JIRA Issue Search MCP Server")
    parser.add_argument("--url", type=str, default=JIRA_API_BASE,
                        help=f"Base URL for the weather API (default: {JIRA_API_BASE})")
    return parser.parse_args()
