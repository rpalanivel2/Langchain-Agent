import asyncio
import streamlit as st

from agent.agent import create_mcp_agent
from agent.invoke import call_agent

async def main():
    st.set_page_config(page_title="Lang-Chat", page_icon="🤖")

    st.title("🤖 Lang-Chat")

    # -----------------------------
    # Sidebar — Context Configuration
    # -----------------------------
    st.sidebar.header("⚙️ Agent Context Settings")

    # Defaults stored in session state
    if "user_id" not in st.session_state:
        st.session_state.user_id = ""
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

    if "agent" not in st.session_state:
        st.session_state.agent = await create_mcp_agent()

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

        agent_reply = await call_agent(st.session_state.agent, user_input)

        st.session_state.chat_history.append(("assistant", agent_reply))
        with st.chat_message("assistant"):
            st.write(agent_reply)


if __name__ == "__main__":
    asyncio.run(main())