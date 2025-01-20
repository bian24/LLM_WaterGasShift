from dotenv import load_dotenv

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import glob
import os
load_dotenv()

# Imports
MODEL = os.getenv("MODEL")

# Relative import for WGS-PDF2 Database
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
pdf_folder_path = os.path.join(parent_dir, 'WGS-PDF1')
pdf_files = glob.glob(f"{pdf_folder_path}/*.pdf")

docs_text = []
for doc in pdf_files:
    loader = PyPDFLoader(doc)
    docs = loader.load()
    docs_text.append(docs[0])

# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs_text)

# vectorstore
vectorstore = Chroma.from_documents(
    documents=all_splits, embedding=OpenAIEmbeddings()
)

# retriever
retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k":5}
)

# model
llm = ChatOpenAI(model=MODEL)

prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
             """
            you are an expert researcher particularly in the field of water gas-shift reactions
            here are some references that you can use to aid in the answering of the questions
            take time in answering, do not give not factual answers
            please try to search throughout the databse of documents that you have first 
            to answer, otherwise if you don't find a clear answer, you're free to search the internet as well
            but you also need to mention from which source do you got it from
            be scientifically accurate in your answer and provide relevant in-depth explanations where you
            deem necessary
            {context}"""),
            ("human", "{input}")
        ]
    )

# chain
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

question = "which metal is the most used in wgs reaction"

responses = rag_chain.invoke({"input": question})
print(responses['answer'])