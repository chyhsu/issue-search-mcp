from .service import make_request
from . import mcp, JIRA_API_BASE

@mcp.tool()
async def sync() -> str | None:
    """Sync the JIRA issue search MCP server."""
    response = await make_request(f"{JIRA_API_BASE}/sync", "POST")
    return f"{response}"

@mcp.tool()
async def query(query_term: str, is_key: bool) -> str | None:
    """Query the JIRA issue search MCP server."""
    if is_key:
        response = await make_request(f"{JIRA_API_BASE}/query?key={query_term}", "GET")
    else:
        response = await make_request(f"{JIRA_API_BASE}/query?q={query_term}", "GET")

    return f"{response}"

@mcp.tool()
async def suggest(key: str) -> str | None:
    """Suggest possible queries for the JIRA issue search MCP server."""
    response = await make_request(f"{JIRA_API_BASE}/suggest?key={key}", "GET")
 
    return f"{response}"