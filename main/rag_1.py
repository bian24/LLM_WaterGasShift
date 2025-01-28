# This file refers to the RAG1 part of the project
# RAG system using the mentioned Database1 of pdf format

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
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

# Relative import for WGS-PDF2 Database
parent_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..'
    )
)
pdf_folder_path = os.path.join(parent_dir, 'WGS-PDF1')
pdf_files = glob.glob(f"{pdf_folder_path}/*.pdf")

docs_text = []
for doc in pdf_files:
    try:

        loader = PyPDFLoader(doc)
        docs = loader.load()

        for page in docs:

            docs_text.append(page)
    except Exception as e:
        print(f"Error loading {doc}: {e}")

# text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs_text)

# Chroma vectorstore
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
            please try to search throughout the database of documents that you have as references and guides
            the answer you might need to come up could possibly come up from multiple files
            so it is possible for you to piece answer together from different files
            you are only allowed to give answers from this particular database
            do not cite papers that do not exist from within these collection of papers
            you are also allowed to make your own reasoning if you have the need to do so
            the pdf files have been named in a way that it contain the names of the author and the year of publication
            be scientifically accurate in your answer and provide relevant in-depth explanations where you deem necessary
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