"""
JIRA Issue Search MCP Server package.
"""

from mcp.server.fastmcp import FastMCP

# Define constants first
JIRA_API_BASE = "https://your-jira-instance.atlassian.net/rest/api/2"
USER_AGENT = "jira-issue-search/1.0"
NWS_API_BASE = "https://api.weather.gov"

# Create the FastMCP instance
mcp = FastMCP("issue-search")

# Now import the modules that need mcp
from .service import make_request, format_alert, parse_args
from .tool import get_alerts, get_forecast

__all__ = ['make_request', 'format_alert', 'get_alerts', 'get_forecast', 'parse_args', 'mcp', 'JIRA_API_BASE']