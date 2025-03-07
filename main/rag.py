# This file serve as the main RAG mechanism purpose for the project
# Can be interchange across different RAG systems by adjusting its designated database

from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
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
MODEL = os.getenv("LLM_MODEL")

# TO BE ADJUSTED FOLDER PATH
# List of Available Folders
# 1. WGS-PDF1: RAG1
# 2. WGS-PDF2: RAG2
# 3. WGS-PDF12: RAG12
# 4. WGS-PDF3: RAG3
PDF_PATH = "WGS-PDF2" 


class RAG:
    def __init__(self):
        self.llm = ChatOpenAI(model = MODEL)
        self.embeddings = OpenAIEmbeddings()
        self.docs = None
        self.vectorstore_dir = f"vectorstore_{PDF_PATH}.db"
        # Check if vectorstore exists
        if os.path.exists(self.vectorstore_dir):
            print("Loading existing vectorstore...")
            self.vectorstore = Chroma(persist_directory=self.vectorstore_dir, embedding_function=OpenAIEmbeddings())
        else:
            print("Creating new vectorstore...")
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            pdf_folder_path = os.path.join(parent_dir, PDF_PATH)
            pdf_files = glob.glob(f"{pdf_folder_path}/*.pdf")
            self.docs = pdf_files

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
                persist_directory=self.vectorstore_dir
            )
            self.vectorstore = vectorstore


    def get_most_relevant_content(self, query):
        """
        Find the most relevant document for a given query.
        """
        
        retrieved_docs = self.vectorstore.similarity_search(query, k=1)
        relevant_content = [doc.page_content for doc in retrieved_docs]

        return relevant_content


    def generate_answer(self, query):
        retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        llm = self.llm

        prompt = ChatPromptTemplate.from_messages([
            ("system", 
            """
            you are an expert researcher particularly in the field of water gas-shift reactions
            here are some references that you can use to aid in the answering of the questions
            take time in answering, do not give not factual answers
            please try to search throughout the database of documents that you have as references and guides
            the answer you might need could possibly come up from multiple files
            so it is possible for you to piece answer together from different files
            you are only allowed to give answers from this particular database
            do not cite sources that do not exist from within these collection of database
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

        responses = rag_chain.invoke({"input": query})
        return responses['answer']
