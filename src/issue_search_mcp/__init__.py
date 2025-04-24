"""
JIRA Issue Search MCP Server package.
"""

from mcp.server.fastmcp import FastMCP


# Create the FastMCP instance
mcp = FastMCP("issue-search")

# Now import the modules that need mcp
from .service import make_request, parse_args, server
from .tool import query, suggest, sync


__all__ = ['make_request', 'query', 'suggest', 'sync', 'parse_args', 'mcp', 'server']