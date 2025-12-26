import langsmith as ls
from agent.agent import create_mcp_agent
from config.config import trace_client

config = {"configurable": {"thread_id": "1"}}

async def call_agent(agent, user_message):  
    if agent is not None:
        with ls.tracing_context(client=trace_client, project_name="Langchain-Agent", enabled=True):
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_message}]},
                config=config
                )
        return response.get("structured_response").response
    return None


