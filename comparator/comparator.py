import csv
import os
from langchain_openai import ChatOpenAI
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import ResponseRelevancy, FactualCorrectness, SemanticSimilarity

# Import
LLM_MODEL = os.getenv("LLM_MODEL")

# TO BE ADJUSTED RAG_FILE PATH
# List of Available Files
# 1. rag_1_script.csv: RAG1
# 2. rag_2_script.csv: RAG2
# 3. rag_12_script.csv: RAG12

FOLDER_PATH = "script"
RAG_VER= "DB_12"
FILE = f"{FOLDER_PATH}/{RAG_VER}"


# Question CSV
question_csv = open(f"{FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)

# Ground Truth CSV
ground_truth_csv = open(f"{FILE}_ground_truth.csv", mode="r", encoding="utf-8")
ground_truth_read = csv.reader(ground_truth_csv)

# Answer CSV
answer_csv = open(f"{FILE}_answer_{LLM_MODEL}_rag.csv", mode="r", encoding="utf-8")
answer_read = csv.reader(answer_csv)

# Dataset Creation
dataset = []
for query, ground_truth, answer in zip(question_read, ground_truth_read, answer_read):
    dataset.append(
        {
            "user_input": query[0],
            "response": answer[0],
            "reference": ground_truth[0]
        }
    )

# Evaluation
evaluation_dataset = EvaluationDataset.from_list(dataset)    
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=LLM_MODEL))
result = evaluate(
    dataset=evaluation_dataset, 
    metrics=[FactualCorrectness(), ResponseRelevancy(), SemanticSimilarity()], 
    llm=evaluator_llm
)

# Dashboard Viewing
result.upload()

# CSV Export
df = result.to_pandas()
folder = os.path.dirname(os.path.abspath(__file__))
df.to_csv(f"{folder}/run_{RAG_VER}_rag_{LLM_MODEL}.csv")