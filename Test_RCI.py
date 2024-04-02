import os
<<<<<<< HEAD
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.llms import openai

os.environ["OpenAI_API_KEY"]

model=openai(model="command", temperature=0.75)
=======
from contants import COHERE_API_KEY
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.llms import Cohere
from langchain.chat_models import ChatCohere
os.environ["COHERE_API_KEY"]=COHERE_API_KEY

model=ChatCohere(model="command", temperature=0.75)
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
prompt=ChatPromptTemplate.from_template("tell me an interasting facts about {subject}")
reverse_prompt=ChatPromptTemplate.from_template("based on this interating fact which is chunked down from a meta subject:\n\n{interasting fact}\n\n Recover what the meta subject is\n Subject:")

chain1=prompt|model| StrOutputParser()
chain2= {"interasting fact":chain1}|reverse_prompt|model|StrOutputParser()
output=chain2.invoke({"subject": "sin square theta + cos square theta = 1"})
print(output)

