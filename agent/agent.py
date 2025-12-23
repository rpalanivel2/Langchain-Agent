from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents.structured_output import ToolStrategy
from langchain.agents.middleware import SummarizationMiddleware

from config.model import model
from tools.tools import client
from models.classmodels import Response
from config.config import checkpointer


async def create_mcp_agent():
    async with client.session("mcpServers") as session:
        tools = await load_mcp_tools(session)

    agent = create_agent(
        model=model,
        tools=tools,
        response_format=ToolStrategy(Response),
        checkpointer=checkpointer,
        middleware=[
            SummarizationMiddleware(
                model=model,
                trigger=("tokens", 4000),
                keep=("messages", 20),
            )
        ],
    )

    return agent
