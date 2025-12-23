from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "mcpServers": {
            "transport": "http",
            "url": "https://docs.langchain.com/mcp",
        }
    }
)