# JIRA Issue Search MCP Server

A specialized MCP server for searching and interacting with JIRA issues. This tool allows you to search for JIRA issues using natural language queries or issue IDs, get suggestions based on issue IDs, and retrieve issues based on specific criteria.

## Tools

- **`query`**: Search for JIRA issues using natural language queries or a specific issue ID.
- **`suggest`**: Get suggestions for related issues based on a specific issue ID.
- **`issues`**: Retrieve issues filtered by assignee and creation date.

## Installation

### Prerequisites

- Python 3.12 or higher
- A running JIRA issue search server

### Install from Source

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd issue-search-mcp
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install the package:
    ```bash
    pip install -e .
    ```

4.  Put the below snippet in the model's mcp config:
    ```json
    {
      "mcpServers": {
        "jira-issue-search": {
          "command": "issue-search-mcp",
          "args": [
            "--url",
            "https://jira-issue-search.dev.myqnapcloud.io/",
            "--token",
            "<YOUR_USER_ACCESS_TOKEN>",
            "--email",
            "<YOUR_EMAIL>"
          ]
        }
      }
    }
    ```

## How to Use

You can use natural language to command the LLM model to utilize the tools.

- **Query Examples:**
  - `"Can you find the issue with ID PROJ-123?"`
  - `"Search for issues with the query term 'login button bug'."`

- **Suggest Examples:**
  - `"Get suggestions for the issue with ID PROJ-123?"`

- **Issues Examples:**
  - `"Search my issues created within the last week."`
  - `"Get issues assigned to 'example@user.com' created after 2024-09-01."`
## Tool Reference

### `query(query_term: str, is_key: bool) -> str | None`

Search for JIRA issues. You can query by a natural language term or a specific issue ID.

- **Parameters**:
  - `query_term`: The search term (natural language query or issue ID).
  - `is_key`: Set to `True` if `query_term` is an issue ID, `False` for natural language queries.
- **Returns**: A formatted string containing issue details or a failure message.

### `suggest(key: str) -> str | None`

Get suggestions based on a specific issue ID.

- **Parameters**:
  - `key`: The JIRA issue ID (e.g., "PROJ-123").
- **Returns**: A suggestion string or a failure message.

### `issues(assignee: str, created_after: str) -> str | None`

Get issues filtered by assignee and creation date.

- **Parameters**:
  - `assignee`: The email of the assignee. If set to `'None'`, it defaults to the email provided in the startup arguments (`--email`).
  - `created_after`: The start date for issue creation (e.g., `"2024-09-01T00:00:00.000+0800"`). Note: This tool only supports `created_after` (not `created_before`) and only retrieves issues created after 2024-09-01.
- **Returns**: A formatted string containing issue details or a failure message.

## Configuration

-   `--url`: The base URL of the JIRA issue search server.
-   `--token`: The bearer token for authenticating with the JIRA issue search server.
-   `--email`: The user's email, used as the default assignee for the `issues` tool.

### Authentication

This MCP server requires authentication with the JIRA issue search API using a bearer token. Provide your user access token via the `--token` command-line parameter.

## Development

### Project Structure

```
issue-search-mcp/
├── src/
│   └── issue_search_mcp/
│       ├── __init__.py      # Package initialization
│       ├── service.py       # Core service functionality and HTTP requests
│       └── tool.py          # MCP tool implementations
├── main.py                  # CLI entry point
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # This documentation
```
