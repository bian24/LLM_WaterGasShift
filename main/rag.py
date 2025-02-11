# This file serve as the main RAG mechanism purpose for the project
# Can be interchange across different RAG systems by adjusting its designated database

from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import glob
import os

load_dotenv()

# IMPORTS

# TO BE ADJUSTED FOLDER PATH
# List of Available Folders
# 1. WGS-PDF1: RAG1
# 2. WGS-PDF2: RAG2
# 3. WGS-PDF12: RAG12
FOLDER_PATH = "WGS-PDF2" 
MODEL = os.getenv("LLM_MODEL")

# Path to store persistent vector database
VECTORSTORE_DIR = f"vectorstore_{FOLDER_PATH}.db"

def load_or_create_vectorstore():
    # Check if vectorstore exists
    if os.path.exists(VECTORSTORE_DIR):
        print("Loading existing vectorstore...")
        vectorstore = Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=OpenAIEmbeddings())
    else:
        print("Creating new vectorstore...")
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        pdf_folder_path = os.path.join(parent_dir, FOLDER_PATH)
        pdf_files = glob.glob(f"{pdf_folder_path}/*.pdf")

        docs_text = []
        for doc in pdf_files:
            try:
                loader = PyPDFLoader(doc)
                docs = loader.load()
                docs_text.extend(docs)
            except Exception as e:
                print(f"Error loading {doc}: {e}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        all_splits = text_splitter.split_documents(docs_text)

        # Create the vectorstore
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=OpenAIEmbeddings(),
            persist_directory=VECTORSTORE_DIR
        )

    return vectorstore

# Load or create vectorstore once during initialization
VECTORSTORE = load_or_create_vectorstore()

def rag(question):
    retriever = VECTORSTORE.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    llm = ChatOpenAI(model=MODEL)

    prompt = ChatPromptTemplate.from_messages([
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
        Remove all characters in this list["*]
        {context}
        """),
        ("human", "{input}")
    ])

    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qa_chain)

    responses = rag_chain.invoke({"input": question})
    return responses['answer']
