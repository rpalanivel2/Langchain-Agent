import langsmith as ls
#from config.config import client
from agent.agent import create_mcp_agent

#trace_client = client
config = {"configurable": {"thread_id": "1"}}

async def call_agent(user_message):  
    #with ls.tracing_context(client=trace_client, project_name="Langchain-Agent", enabled=True):
    agent = await create_mcp_agent()
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": user_message}]},
        config=config
        )
    return response.get("structured_response").response


if __name__ == "__main__":
    import asyncio

    user_message = "How to create an agent in python?"
    response = asyncio.run(call_agent(user_message))
    print("Agent Response:", response)
