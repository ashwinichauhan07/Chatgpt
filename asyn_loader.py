
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores.milvus import Milvus
from langchain_community.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

# Access variables using os.getenv()
OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")
# bs4_strainer = bs4.SoupStrainer('div',{'class': 'theme-doc-markdown markdown'})
urls = ["https://python.langchain.com/docs/get_started/introduction", ]
loader = WebBaseLoader(urls)
docs = loader.load()
# Transform
# from langchain_community.document_transformers import Html2TextTransformer

# html2text = Html2TextTransformer()
# docs_transformed = html2text.transform_documents(docs)
# docs_transformed[0].page_content[0:500]
# print(docs)

# len(docs[0].page_content)
# print(docs[0].page_content[:500])
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
# all_splits[1].metadata
# print(all_splits)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
template="""You are a kind AI agent, you are currently talking to human answer him/her in a friendly tone. and you know many indian language also and respond in indian language 
    
    human:{question}
    AI: """

prompt = PromptTemplate.from_template(template)
COLLECTION_NAME = 'doc_qa_db'
DIMENSION = 786
URI = 'https://in03-86febedb9550389.api.gcp-us-west1.zillizcloud.com'
TOKEN = 'b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886'
connection_args = { 'uri': URI, 'token': TOKEN }



vectorstore = Milvus.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(),
                                    collection_name=COLLECTION_NAME,
                                    connection_args=connection_args,
                                    )
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | llm
    |prompt

)
response=chain.invoke("What is langchain ?")

print(response)