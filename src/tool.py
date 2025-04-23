from .service import make_request
from . import mcp, JIRA_API_BASE

@mcp.tool()
async def sync() -> str | None:
    """Sync the JIRA issue search MCP server."""
    response = await make_request(f"{JIRA_API_BASE}/sync", "POST")
    return f"{response}"

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
    
    result_str="\n---\n".join(f"{issue}" for issue in response['result'])
   
    
    return result_str

@mcp.tool()
async def suggest(key: str) -> str | None:
    """Suggest possible queries for the JIRA issue search MCP server.
    
    Args:
        key: ID of the issue to be suggested 
    """
    response = await make_request(f"{JIRA_API_BASE}/suggest?key={key}", "GET")
    return f"{response['result']}"