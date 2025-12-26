import os
from dotenv import load_dotenv

import langsmith as ls
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

load_dotenv()

API_KEY = os.getenv('TRACING_KEY')

# Tracing client configuration
trace_client = ls.Client(
    api_key=API_KEY,  # This can be retrieved from a secrets manager
    api_url="https://api.smith.langchain.com",  # Update appropriately for self-hosted installations or the EU region
)