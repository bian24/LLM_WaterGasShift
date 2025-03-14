# This file serve as the main RAG mechanism purpose for the project
# Can be interchange across different RAG systems by adjusting its designated database

from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.listwise_rerank import LLMListwiseRerank

import glob
import os

load_dotenv()

# IMPORTS
LLM_MODEL = os.getenv("LLM_MODEL")

# TO BE ADJUSTED FOLDER PATH
# List of Available Folders
# 1. WGS-PDF1: RAG1
# 2. WGS-PDF2: RAG2
# 3. WGS-PDF12: RAG12
# 4. WGS-PDF3: RAG3
PDF_PATH = "WGS-PDF2" 


class RAG:
    def __init__(self):
        self.docs = None
        self.llm = None
        self.vectorstore_dir = f"vectorstore_{PDF_PATH}.db"
        
        # LLM Selection
        if "gpt" in LLM_MODEL:
            self.llm = ChatOpenAI(model = LLM_MODEL)
            self.embeddings = OpenAIEmbeddings()
        if "llama" in LLM_MODEL:
            self.llm = ChatOllama(model = LLM_MODEL)
            self.embeddings = OllamaEmbeddings(model = LLM_MODEL)
        
        # Vectorstore verification
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

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200, add_start_index=True)
            all_splits = text_splitter.split_documents(docs_text)

            # Create the vectorstore
            self.vectorstore = Chroma.from_documents(
                documents=all_splits,
                embedding=self.embeddings,
                persist_directory=self.vectorstore_dir
            )


    def get_most_relevant_content(self, query):
        
        llm = self.llm
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 2})
        
        
        ranker = LLMListwiseRerank.from_llm(llm, top_n=5)
        retriever = ContextualCompressionRetriever(
            base_compressor=ranker,
            base_retriever=retriever
        )
        
        compressed_docs = retriever.invoke(query)
        compressed_content = " ".join([doc.page_content for doc in compressed_docs])

        return compressed_content
        
    
    def generate_answer(self, query):
        # Initialize
        llm = self.llm
        retriever = self.vectorstore.as_retriever(search_kwargs={'k': 5})

        # Filter and Compress
        filter = LLMListwiseRerank.from_llm(llm, top_n=10)
        retriever = ContextualCompressionRetriever(
            base_compressor=filter,
            base_retriever=retriever
        )

        compressed_docs = retriever.invoke(query)
        compressed_context = " ".join([doc.page_content for doc in compressed_docs])


        prompt_text="""
        you are an expert researcher particularly in the field of water gas-shift reactions
        here are some references that you can use to aid in the answering of the questions
        {context}
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
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_text),
            ("human", "{input}")
        ])

        # chain creation
        qa_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, qa_chain)
        answer = rag_chain.invoke({"input": query, "context": compressed_context})['answer']
       
        return answer
