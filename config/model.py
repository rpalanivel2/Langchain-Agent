from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

model = AzureChatOpenAI(
    model=os.getenv('AZURE_DEPLOYMENT_MODEL'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_API_VERSION'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    # azure_deployment_name = os.getenv('AZURE_DEPLOYMENT_MODEL'),
    temperature=0.1
)