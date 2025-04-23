from typing import Any
import httpx
import argparse
from . import JIRA_API_BASE, USER_AGENT
import os


async def make_request(url: str, method: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    # Get absolute path for logs file
    logs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs.txt")
    
    # Log the request attempt
    with open(logs_path, "a") as f:
        f.write(f"\nAttempting {method} request to: {url}\n")
    
    headers = {
        "User-Agent": USER_AGENT
    }
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, timeout=30.0)
            elif method == "POST":
                response = await client.post(url, headers=headers, timeout=30.0)
            
            # Log the response status
            with open(logs_path, "a") as f:
                f.write(f"Response status: {response.status_code}\n")
            
            response.raise_for_status()
            
            # Log success
            with open(logs_path, "a") as f:
                f.write(f"Request successful, parsing JSON response\n")
            
            return response.json()
        except httpx.HTTPStatusError as e:
            # Log HTTP errors
            with open(logs_path, "a") as f:
                f.write(f"HTTP error: {e.response.status_code} - {e.response.text}\n")
            return None
        except httpx.RequestError as e:
            # Log request errors
            with open(logs_path, "a") as f:
                f.write(f"Request error: {str(e)}\n")
            return None
        except Exception as e:
            # Log unexpected errors
            with open(logs_path, "a") as f:
                f.write(f"Unexpected error: {str(e)}\n")
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
