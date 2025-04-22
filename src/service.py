from typing import Any
import httpx
import argparse
from . import JIRA_API_BASE, USER_AGENT



async def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="JIRA Issue Search MCP Server")
    parser.add_argument("--url", type=str, default=JIRA_API_BASE,
                        help=f"Base URL for the weather API (default: {JIRA_API_BASE})")
    return parser.parse_args()

