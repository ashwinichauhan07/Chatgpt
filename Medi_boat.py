import os
from contants import COHERE_API_KEY
from langchain.llms import Cohere
from langchain.prompts import StringPromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool, AgentExecutor,LLMSingleActionAgent,AgentOutputParser
from langchain.tools import DuckDuckGoSearchRun
from typing import List,Union
from langchain.schema import AgentAction, AgentFinish
import re
import langchain
os.environ["COHERE_API_KEY"]=COHERE_API_KEY

search= DuckDuckGoSearchRun()
tools=[
    Tool(
        name="search",
        func= search.run,
        description="useful that when you need to answer question about current events"

    )]
obj=search.run("How can I treat a sprained ankle?")
type(obj)
print(obj)