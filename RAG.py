import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.redis import Redis
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.milvus import Milvus

import os


from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

# Access variables using os.getenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
llm=ChatOpenAI(api_key=COHERE_API_KEY)
    
template="""You are a kind AI agent, you are currently talking to human answer him/her in a friendly tone. and you know many indian language also and respond in indian language 
    
    human:{question}
    AI: """

prompt = PromptTemplate.from_template(template)
COLLECTION_NAME = 'doc_qa_db'
DIMENSION = 786
URI = 'https://in03-86febedb9550389.api.gcp-us-west1.zillizcloud.com'
TOKEN = 'b4b4ed0dc810e8718d8b7c27241b2ad0e2941d239be8cd3a7a1aa9e04dc33c9ae35ef4e4d9dad56fd0ffb9f8d8902e5312064886'
connection_args = { 'uri': URI, 'token': TOKEN }# Only keep post title, headers, and content from the full HTML.
bs4_strainer = bs4.SoupStrainer('div',{'class': 'theme-doc-markdown markdown'})

loader = WebBaseLoader(
    web_paths=("https://python.langchain.com/docs/get_started/introduction",
               ),
    bs_kwargs={"parse_only": bs4_strainer},
)

docs = loader.load()
len(docs[0].page_content)
# print(docs[0].page_content[:500])
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=50, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)
# all_splits[1].metadata
# print(all_splits)

vectorstore = Milvus.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(),
                                    collection_name=COLLECTION_NAME,
                                    connection_args=connection_args,
                                    )
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
# # chains = (
# #     {"context": retriever | format_docs, "question": RunnablePassthrough()}
# #     )
# # chain=LLMChain(
# #     llm=llm,
# #     prompt=prompt,
# #     verbose=True,
# #     chain= chains
# # )

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
response=chain.invoke("What is langchain ?")

print(response)


