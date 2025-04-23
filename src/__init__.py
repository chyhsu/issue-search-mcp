"""
JIRA Issue Search MCP Server package.
"""

from mcp.server.fastmcp import FastMCP

# Define constants first
JIRA_API_BASE = "http://127.0.0.1:6060"


# Create the FastMCP instance
mcp = FastMCP("issue-search")

# Now import the modules that need mcp
from .service import make_request, parse_args
from .tool import get_forecast

__all__ = ['make_request', 'get_forecast', 'parse_args', 'mcp', 'JIRA_API_BASE']