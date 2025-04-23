import src  


def main():
    args = src.parse_args()
    print("Hello from issue-search-mcp!")
    
    # Update the module's JIRA_API_BASE variable
    src.JIRA_API_BASE = args.url
    print(f"Using API URL: {src.JIRA_API_BASE}")
    
    # Run the MCP server
    src.mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
