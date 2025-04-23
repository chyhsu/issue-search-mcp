# JIRA Issue Search MCP Server

A specialized MCP server for searching and interacting with JIRA issues. This tool allows you to search for JIRA issues using natural language queries or issue IDs, get suggestions based on issue IDs, and synchronize with the JIRA issue search server.

## Tools

- **Query**: Search for JIRA issues using either:
  - Natural language queries
  - Specific issue IDs
- **Suggest**: Get suggestions based on a specific issue ID
- **Sync**: Synchronize the local database with the JIRA issue search server

## Installation

### Prerequisites

- Python 3.12 or higher
- A running JIRA issue search server 

### Install from Source

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd issue-search-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

4. Put the below snippet in the model's mcp config:
   ```json
   {
     "mcpServers": {
       "jira-issue-search": {
         "command": "issue-search-mcp",
         "args": [
           "--url",
           "<JIRA_API_BASE_URL>"
         ]
       }
     }
   }
   ```

## Usage

### As a Command-Line Tool

After installation, you can run the MCP server:

```bash
issue-search-mcp [--url JIRA_API_BASE_URL]
```


### As a Python Module

```python
from issue_search_mcp import query, suggest, sync

# Query JIRA issues
result = await query("performance issue", is_key=False)  # Natural language query
result = await query("PROJ-123", is_key=True)  # Issue ID query

# Get suggestions for an issue
suggestions = await suggest("PROJ-123")

# Synchronize with JIRA server
sync_result = await sync()
```

## Tool Reference

### `query(query_term: str, is_key: bool) -> str | None`

Search for JIRA issues.

- **Parameters**:
  - `query_term`: The search term (natural language query or issue ID)
  - `is_key`: Set to `True` if `query_term` is an issue ID, `False` for natural language queries
- **Returns**: Formatted string containing issue details or "Action Failed" if the request fails

### `suggest(key: str) -> str | None`

Get suggestions based on a specific issue ID.

- **Parameters**:
  - `key`: The JIRA issue ID (e.g., "PROJ-123")
- **Returns**: Suggestion string or "Action Failed" if the request fails

### `sync() -> str | None`

Synchronize with the JIRA issue search server.

- **Returns**: Status message including updated issues or "Action Failed" if the request fails

## Configuration

The default JIRA API base URL is `http://127.0.0.1:6060`. You can change this by:

1. Using the `--url` command-line parameter
2. Modifying the `JIRA_API_BASE` constant in the `__init__.py` file

## Development

### Project Structure

```
issue-search-mcp/
├── src/
│   └── issue_search_mcp/
│       ├── __init__.py      # Package initialization and constants
│       ├── service.py       # Core service functionality and HTTP requests
│       └── tool.py          # MCP tool implementations (query, suggest, sync)
├── main.py                  # Entry point for direct execution
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # This documentation
```

### Dependencies

- `httpx`: For asynchronous HTTP requests
- `mcp[cli]`: MCP server framework
- `argparse`: Command-line argument parsing
- `typing`: Type annotations
- `json5`: JSON parsing


