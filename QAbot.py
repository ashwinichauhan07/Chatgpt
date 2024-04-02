<<<<<<< HEAD
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
import os
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()
OpenAI_API_KEY = os.getenv("OpenAI_API_KEY")

#web scraping 

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125",  api_key=OpenAI_API_KEY)

loader = WebBaseLoader('https://python.langchain.com/docs/get_started/introduction')
docs = loader.load()
# print(docs)
# bs_transformer = BeautifulSoupTransformer()
# docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["p"])
    # print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000,
                                                                    chunk_overlap=0)
splits = splitter.split_documents(docs)
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

retriever = vectorstore.as_retriever(search_type="similarity")




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
response2=chain2.invoke("langchain model ")

print(response2)
=======
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("F:/Books/DSML.pdf")
import os

print(os.environ.get("OPENAI_API_KEY"))  # Should print your API key


#Load the document by calling loader.load()
pages = loader.load()

print(len(pages))
print(pages[0].page_content[0:500])

print(pages[0].metadata)

from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)

#Create a split of the document using the text splitter
splits = text_splitter.split_documents(pages)

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()

persist_directory = 'pages/chroma/'

# Create the vector store
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

print(vectordb._collection.count())
>>>>>>> facccae66ed0241c2782eed4e3f3c8842aaefdd1
