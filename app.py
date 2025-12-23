import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel

import langsmith as ls
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from config.config import trace_client

load_dotenv()

# Define response schema
class Response(BaseModel):
    response: str


# Initialize MCP client
client = MultiServerMCPClient(
    {
        "docs-langchain": {
            "transport": "http",
            "url": "https://docs.langchain.com/mcp",
        }
    }
)

# Initialize Azure OpenAI model
azure_model = AzureChatOpenAI(
    model=os.getenv('AZURE_DEPLOYMENT_MODEL'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_API_VERSION'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    temperature=0.1
)

checkpointer = InMemorySaver()

# Async function to run agent
async def run_agent(user_input: str):
    async with client.session("docs-langchain") as session:
        config = {"configurable": {"thread_id": "1"}}
        tools = await load_mcp_tools(session)
        agent = create_agent(
            tools=tools,
            model=azure_model,
            response_format=ToolStrategy(Response),
            checkpointer=checkpointer,
        )
        with ls.tracing_context(client=trace_client, project_name="Langchain-Agent", enabled=True):
            response = await agent.ainvoke({"messages": [{"role": "user", "content": user_input}]}, config=config,)
        return response.get("structured_response").response

# Streamlit UI
st.set_page_config(page_title="Langchain Agent", page_icon="🤖")

st.title("🤖 Langchain Agent")

# -----------------------------
# Sidebar — Context Configuration
# -----------------------------
st.sidebar.header("⚙️ Agent Context Settings")

# Defaults stored in session state
if "user_id" not in st.session_state:
    st.session_state.user_id = "123"
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

st.session_state.user_id = st.sidebar.text_input(
    "User ID",
    value=st.session_state.user_id,
)

st.session_state.user_name = st.sidebar.text_input(
    "User Name",
    value=st.session_state.user_name,
)

st.sidebar.write("---")
st.sidebar.write("These values are passed to the agent on every message.")


# -----------------------------
# Chat UI
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(msg)

# Chat input area
user_input = st.chat_input("Type your message…")

# When the user sends a message
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    agent_reply = asyncio.run(run_agent(user_input))

    st.session_state.chat_history.append(("assistant", agent_reply))
    with st.chat_message("assistant"):
        st.write(agent_reply)