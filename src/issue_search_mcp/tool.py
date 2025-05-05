import issue_search_mcp.service as srv
from . import mcp

@mcp.tool()
async def sync() -> str | None:
    """Sync the JIRA issue search MCP server."""
    response = await srv.make_request("sync", "POST")

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
        response = await srv.make_request(f"query?key={query_term}", "GET")
    else:
        response = await srv.make_request(f"query?q={query_term}", "GET")
    
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
        issue_type = issue.get('issuetype')
        description = issue.get('description')
        status = issue.get('status')
        assignee = issue.get('assignee')
        formatted.append(f"key: {key}  summary: {summary}  url: {url}  created_at: {created}  issue_type: {issue_type}  description: {description}  status: {status}  assignee: {assignee}")
    result_str = "\n---\n".join(formatted)
    return result_str

@mcp.tool()
async def suggest(key: str) -> str | None:
    """Suggest possible queries for the JIRA issue search MCP server.
    
    Args:
        key: ID of the issue to be suggested 
    """
    response = await srv.make_request(f"suggest?key={key}", "GET")
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
        assignee: Email of the Assignee of the issue. This parameter could be None, then it will use the default email after "--email". For example, "assignee = 'None'" or "assignee = 'abcdef@qnap.com'".
        created_after: Created after date, for example "2025-04-01T15:19:03.000+0800"
    """
    if assignee=="None":
        assignee = srv.EMAIL

    response = await srv.make_request(f"get_issues?assignee={assignee}&created_after={created_after}", "GET")
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
        issue_type = issue.get('issuetype')
        description = issue.get('description')
        status = issue.get('status')
        assignee = issue.get('assignee')
        formatted.append(f"key: {key}  summary: {summary}  url: {url}  created_at: {created}  issue_type: {issue_type}  description: {description}  status: {status}  assignee: {assignee}")
    result_str = "\n---\n".join(formatted)
    return result_str