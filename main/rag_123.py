from dotenv import load_dotenv
import glob
from langchain.agents import initialize_agent, AgentType
from langchain.chains import retrieval_qa
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import Tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import pickle
import xgboost


from crf import process_input

load_dotenv()


# Imports
XGB_MODEL = os.getenv("XGB_MODEL")


class RAG3:
    def __init__(self, DB, LLM_MODEL):
        self.docs = None
        self.llm = LLM_MODEL
        self.model = pickle.load(open(XGB_MODEL, "rb"))
        self.vectorstore_dir = f"vectorstore_{DB}_{LLM_MODEL}.db"
        
        # Feature categories
        self.feature_categories = {
        "metals": ['Platinum', 'Gold', 'Ruthenium', 'Rhodium', 'Iridium', 'Copper', 'Palladium', 'Nickel', 'Osmium', 'Rhenium'],
        "supports": [
            'Aluminum Oxide', 'Magnesium Oxide', 'Cerium Oxide', 'Titanium Dioxide', 
            'Titanium Dioxide P25', 'Manganese Oxide', 'Yttrium Oxide', 'Zirconium Oxide', 
            'Hydroxyapatite', 'Amorphous Calcium Carbonate', 'Hafnium Oxide', 
            'Lanthanum Oxide', 'Cobalt Oxide', 'Silicon Dioxide', 'Zinc Oxide', 
            'Magnetite (Iron(II,III) Oxide)', 'Hematite (Iron(III) Oxide)', 
            'Calcium Oxide', 'Ruthenium Dioxide', 'Gallium Oxide', 'Uranium Trioxide', 
            'Triuranium Octoxide', 'Chromium(III) Oxide', 'Manganese Dioxide', 
            'Graphene Oxide', 'Alpha Molybdenum Carbide', 'Molybdenum Nitride'
        ],
        "promoters": [
            'Lithium', 'Cerium', 'Cobalt', 'Iron', 'Manganese', 'Zirconium', 'Potassium', 
            'Nickel', 'Cesium', 'Rubidium', 'Yttrium', 'Sodium', 'Lanthanum', 'Gadolinium', 
            'Praseodymium', 'Zinc'
        ],
        "methods": [
            'Impregnation with Inverse Water', 'Wet Impregnation', 'Chemical Impregnation', 
            'Solid Impregnation', 'Sol-Gel Process', 'Co-precipitation', 'High-Density Plasma', 
            'Ultrasonic Gelation Coating', 'Solid State Combustion', 'Flame Spray Pyrolysis', 
            'Mechanochemical Synthesis', 'Dip Coating', 'Ultraviolet Curing', 'Thermal Decomposition', 
            'Self-Combustion Method', 'Direct Ammonia Synthesis', 'Hydrothermal Synthesis', 
            'Thermal Co-precipitation', 'Direct Current Plasma', 'Low-Pressure Reduction Deposition', 
            'Chemical Vapor Deposition', 'Rapid Solidification of Thermal Deposition', 
            'Milling Process', 'Hydrothermal Method', 'Nanocasting', 'Evaporation-Induced Self-Assembly', 
            'Chemical Adsorption', 'Chemical Deposition', 'Ultrasonic Spray Method', 'Plasma Treatment', 
            'Acoustic Emission Heating', 'Acid Precipitation'
        ],
        "catalysts": [
        'Krypton', 'Carbon Monoxide', 'Water', 'Carbon Dioxide', 'Hydrogen', 
        'Oxygen', 'Methane', 'Nitrogen', 'Helium', 'Argon'
        ],
        "parameters": ['temperature', 'TOS', 'W/F']
        }
        self.num_features = sum(len(v) for v in self.feature_categories.values())
        
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
            self.vectorstore = Chroma(persist_directory=self.vectorstore_dir, embedding_function=self.embeddings)
        else:
            print("Creating new vectorstore...")
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            pdf_folder_path = os.path.join(parent_dir, DB)
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

        # Define LangChain Agent
        self.agent = initialize_agent(
            tools=[
                Tool(name="CRF Extractor", func=self.extract_features, description="Extracts a 98x1 feature vector from input text."),
                Tool(name="Feature Validator", func=self.validate_features, description="Checks for missing or unrealistic feature values."),
                Tool(name="RAG Retriever", func=self.query_rag, description="Retrieves missing feature values from the RAG knowledge base."),
            ],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Uses reasoning to decide which tool to use
            verbose=True
        )
    
    
    def extract_features(self, query):
        """Extracts features using the CRF model."""
        elements_array = process_input(query) 

        return elements_array

    def query_rag(self, missing_features):
        """
        Queries RAG for missing features.
        """
        query = f"Provide information on {', '.join(missing_features)}"
        retrieved_info = self.retriever.run(query)

        return retrieved_info
    

    def crf_extract(self, query):
        """
        Uses CRF to extract relevant features, queries RAG if any are missing,
        and predicts CO conversion using XGBoost.
        """
        elements_array = process_input(query)
        prediction = self.model.predict([elements_array])
        print(elements_array)
        missing_features = []
        if elements_array.get("catalyst") is None:
            missing_features.append("catalyst")
        if elements_array.get("temperature") is None:
            missing_features.append("temperature")
        if elements_array.get("W/F ratio") is None:
            missing_features.append("W/F ratio")

        if missing_features:
            rag_data = self.query_rag(missing_features)
            print(f"RAG retrieved: {rag_data}")

            for feature in missing_features:
                elements_array[feature] = rag_data.get(feature, None)

        prediction = self.model.predict([elements_array])

        return prediction[0]

        

