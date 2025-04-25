from .service import make_request
from . import mcp

@mcp.tool()
async def sync() -> str | None:
    """Sync the JIRA issue search MCP server."""
    response = await make_request("sync", "POST")

    if not response:
        return "Action Failed"
    if response.get('status') == 401:
        return response.get('message', 'Unauthorized')
    
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
        response = await make_request(f"query?key={query_term}", "GET")
    else:
        response = await make_request(f"query?q={query_term}", "GET")
    
    if not response:
        return "Action Failed"
    if response.get('status') == 401:
        return response.get('message', 'Unauthorized')
    if response.get('message') == "No Result":
        return "Issue not found"
    
    items = response['results']
    formatted = []
    for issue in items:
        key = issue.get('key')
        summary = issue.get('summary')
        url = issue.get('url')
        created = issue.get('created')
        issue_type = issue.get('issue_type')
        description = issue.get('description')
        assignee = issue.get('assignee')
        formatted.append(f"key: {key}  summary: {summary}  url: {url}  created_at: {created}  issue_type: {issue_type}  description: {description}  assignee: {assignee}")
    result_str = "\n---\n".join(formatted)
    return result_str

@mcp.tool()
async def suggest(key: str) -> str | None:
    """Suggest possible queries for the JIRA issue search MCP server.
    
    Args:
        key: ID of the issue to be suggested 
    """
    response = await make_request(f"suggest?key={key}", "GET")
    if not response:
        return "Action Failed"
    if response.get('status') == 401:
        return response.get('message', 'Unauthorized')
    if response.get('message') == "No Result":
        return "Issue not found"
    result_str = f"{response['results']['suggestion']}"
    return result_str

@mcp.tool()
async def issues(created_after: str, assignee: str) -> str | None:
    """Get issues from the JIRA issue search MCP server.
    
    Args:
        assignee: Assignee of the issue, could be None,default is the email after "--email", for example "jasoncyhsu@qnap.com"
        created_after: Created after date, for example "2025-04-01T15:19:03.000+0800"
    """
    if not assignee:
        assignee = EMAIL

    response = await make_request(f"get_issues?assignee={assignee}&created_at={created_after}", "GET")
    if not response:
        return "Action Failed"
    if response.get('status') == 401:
        return response.get('message', 'Unauthorized')
    if response.get('message') == "No Result":
        return "No issues found"
    items = response['results']
    formatted = []
    for issue in items:
        key = issue.get('key')
        summary = issue.get('summary')
        url = issue.get('url')
        created = issue.get('created')
        issue_type = issue.get('issue_type')
        description = issue.get('description')
        assignee = issue.get('assignee')
        formatted.append(f"key: {key}  summary: {summary}  url: {url}  created_at: {created}  issue_type: {issue_type}  description: {description}  assignee: {assignee}")
    result_str = "\n---\n".join(formatted)
    return result_str