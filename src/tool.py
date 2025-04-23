from .service import make_request
from . import mcp, JIRA_API_BASE

@mcp.tool()
async def sync() -> str | None:
    """Sync the JIRA issue search MCP server."""
    response = await make_request(f"{JIRA_API_BASE}/sync", "POST")
    if not response:
        return "Action Failed"
    result_str= f"message: {response['message']}, updated:"
    for issue in response['updated']:
        result_str += f" {issue},"
    return result_str

@mcp.tool()
async def query(query_term: str, is_key: bool) -> str | None:
    """Query the JIRA issue search MCP server.
    
    Args:
        query_term: The query term to search for which can be an issue ID or a natural language query
        is_key: Whether the query term is an issue ID
    """
    if is_key:
        response = await make_request(f"{JIRA_API_BASE}/query?key={query_term}", "GET")
    else:
        response = await make_request(f"{JIRA_API_BASE}/query?q={query_term}", "GET")
    
    if not response:
        return "Action Failed"

    items = response['results']
    formatted = []
    for issue in items:
        key = issue.get('key')
        summary = issue.get('summary')
        url = issue.get('url')
        created = issue.get('created')
        formatted.append(f"key: {key}  summary: {summary}  url: {url}  created_at: {created}")
    result_str = "\n---\n".join(formatted)
    return result_str

@mcp.tool()
async def suggest(key: str) -> str | None:
    """Suggest possible queries for the JIRA issue search MCP server.
    
    Args:
        key: ID of the issue to be suggested 
    """
    response = await make_request(f"{JIRA_API_BASE}/suggest?key={key}", "GET")
    if not response:
        return "Action Failed"
    result_str = f"suggestion: {response['results']['suggestion']}, description: {response['results']['description']}"
    return result_str