from typing import Any
import httpx
import argparse
from . import mcp,TOKEN


async def make_request(url: str, method: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        try:
            if method == "GET":
                response = await client.get(url, timeout=30.0, headers=headers)
            elif method == "POST":
                response = await client.post(url, timeout=90.0, headers=headers)
            
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
    parser.add_argument("--url", type=str, 
                        help=f"Base URL for the JIRA-issue-search MCP server")
    parser.add_argument("--token", type=str, help=f"Token for the JIRA-issue-search MCP server")
    return parser.parse_args()

def server():
    args = parse_args()
    print("Hello from JIRA-issue-search MCP server!")
    
    # Update the module's JIRA_API_BASE variable
    JIRA_API_BASE = args.url

    # Update the module's TOKEN variable
    TOKEN = args.token
    
    print(f"Using API URL: {JIRA_API_BASE}")
    
    # Run the MCP server
    mcp.run(transport='stdio')
