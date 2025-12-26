from langchain_mcp_adapters.client import MultiServerMCPClient


client = MultiServerMCPClient(
    {
        "docs-langchain": {
            "transport": "http",
            "url": "https://docs.langchain.com/mcp",
        }
    }
)