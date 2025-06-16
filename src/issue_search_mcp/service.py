import argparse
import httpx
from typing import Any
from . import mcp

# Define constants first
JIRA_API_BASE = None
TOKEN = None
EMAIL = None

async def make_request(url: str, method: str) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

        if method == "GET":
            resp = await client.get(f"{JIRA_API_BASE}/{url}", timeout=300.0, headers=headers)
        elif method == "POST":
            resp = await client.post(f"{JIRA_API_BASE}/{url}", timeout=600.0, headers=headers)
        else:                         # guard against typos
            raise ValueError(f"Unsupported method {method}")

        resp.raise_for_status()
        return resp.json()

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="JIRA Issue Search MCP Server")
    p.add_argument("--url", required=True,  type=str,
                   help="Base URL for the JIRA-issue-search MCP server")
    p.add_argument("--token", type=str,
                   help="Bearer token for the JIRA-issue-search MCP server")
    p.add_argument("--email", type=str,
                   help="Email of the user of the JIRA-issue-search MCP server")
    return p.parse_args()

def server() -> None:

    args = parse_args()
    print("Hello from JIRA-issue-search MCP server!")

    # tell Python we want to *update* the module-level vars, not shadow them
    global TOKEN, JIRA_API_BASE, EMAIL
    JIRA_API_BASE = args.url
    TOKEN         = args.token
    EMAIL         = args.email

    print(f"Using API URL: {JIRA_API_BASE}")
    print(f"Using Token  : {TOKEN or '<none>'}")
    print(f"Using Email  : {EMAIL or '<none>'}")

    mcp.run(transport="stdio")


def assign_fields(issue)->str:


    key = issue.get('key')
    summary = issue.get('summary')
    url = issue.get('url')
    created = issue.get('created')
    issue_type = issue.get('issuetype')
    description = issue.get('description')
    status = issue.get('status')
    assignee = issue.get('assignee')
    comment = issue.get('comment')

    return f"key: {key}  summary: {summary}  url: {url}  created_at: {created}  issue_type: {issue_type}  description: {description}  status: {status}  assignee: {assignee}  comment: {comment}"

