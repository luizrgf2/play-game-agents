import os
from config import LLM_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph
from tools.print_game import screenshot_tool

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = LLM_API_KEY

__LLM: ChatGoogleGenerativeAI = None
__REACT_AGENT: CompiledGraph = None

def google_llm():
    global __LLM
    if __LLM != None:
        return __LLM

    __LLM = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

def get_react_agent():
    global __REACT_AGENT
    if __REACT_AGENT != None:
        return __REACT_AGENT
    
    tools = [screenshot_tool]

    if  __LLM == None:
        google_llm()
    __REACT_AGENT = create_react_agent(__LLM, tools=tools)
    return __REACT_AGENT
