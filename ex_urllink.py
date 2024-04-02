import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores.milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()
OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")

#web scraping 

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125",  api_key=OpenAI_API_KEY)

# loader = WebBaseLoader('https://python.langchain.com/docs/get_started/introduction')
# docs = loader.load()
url=""
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
    # Example: Extract all paragraph texts; adjust this to your needs
paragraphs = soup.find_all('p')

# Convert the ResultSet of <p> tags into a single string
# Join the text of each paragraph, separating them with a space or newline
combined_text = ' '.join(p.get_text() for p in paragraphs)

    # Grab the first 1000 tokens of the site
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=100,
                                                                    chunk_overlap=0)
splits = splitter.split_text(combined_text)
# print(splits)
COLLECTION_NAME = 'doc_qa_db'
DIMENSION = 786
URI = 'https://in03-7dc3ad7601f794a.api.gcp-us-west1.zillizcloud.com'
TOKEN = 'f493dfbf7234405509db30985647e241d0c4a0ca2969d5261ee6ae1946303ac56c1ed15e923f430edd19cd2d7343c1d7e8b6771b'
connection_args = { 'uri': URI, 'token': TOKEN }



vectorstore = Milvus.from_documents(documents=splits, embedding=OpenAIEmbeddings(),
                                    collection_name=COLLECTION_NAME,
                                    connection_args=connection_args,
                                    )

# retrive from vector
retriever =[]

retriever = vectorstore.as_retriever(search_type="similarity",
        search_kwargs={'k': 5, 'fetch_k': 50})


# print('retriver',retriever)
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

template=""" give similer answer for given question 
    
    human:{question}
    AI: """
prompt = PromptTemplate.from_template(template)

chain = (
    {"context": retriever , "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
response=chain.invoke("what is langchain  ?")

print(response)


chain2 = (
    {"context": retriever , "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
response2=chain2.invoke("what is langchain  ?")

print(response2)