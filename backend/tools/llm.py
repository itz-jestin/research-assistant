from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY


llm = ChatOpenAI(
    model="meta/llama-3.1-8b-instruct",
    api_key=OPENAI_API_KEY,
    base_url="https://integrate.api.nvidia.com/v1",
    temperature=0
)