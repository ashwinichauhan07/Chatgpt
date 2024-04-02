import os
from contants import COHERE_API_KEY
from langchain.llms import Cohere

from langchain import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chat_models import ChatCohere
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
os.environ["COHERE_API_KEY"]=COHERE_API_KEY

model=ChatCohere(model="command", temperature=0.75)

template= "you are a helpful assistant that imports wisdom and guides people with accurate answer"
system_message_prompt=SystemMessagePromptTemplate.from_template(template)
human_template="{question}"
human_message_prompt=HumanMessagePromptTemplate.from_template(human_template)
chat_prompt=ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain1= chat_prompt|model|StrOutputParser()

<<<<<<< HEAD
initial_question="Langchain"
=======
initial_question="sin square theta + cos square theta = 1?"
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1

initial_answer=chain1.invoke({"question":initial_question})
print(initial_answer)