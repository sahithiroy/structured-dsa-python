'''from langchain.agents import create_agent

agent = create_agent(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    tools=[],
    system_prompt="""
    You are a helpful assistant that answers questions using Google search results.
    Always use the search tool to find the most up-to-date information.
    """
)
print(agent)

from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

response = llm.invoke("What is LangChain?")
print(response.content)


'''

'''
Multi Search Agent RAG:
1.Tools---> Toolkit
'''
