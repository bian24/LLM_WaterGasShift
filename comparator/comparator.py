import csv
import os
from langchain_openai import ChatOpenAI
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import RougeScore, StringPresence, FactualCorrectness

from main.rag import RAG


# Import
MODEL = os.getenv("LLM_MODEL")

# TO BE ADJUSTED RAG_FILE PATH
# List of Available Files
# 1. rag_1_script.csv: RAG1
# 2. rag_2_script.csv: RAG2
# 3. rag_12_script.csv: RAG12

FOLDER_PATH = "script"
RAG_VER= "rag_2"
FILE = f"{FOLDER_PATH}/{RAG_VER}"


# Question and Answer CSV
question_csv = open(f"{FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)
ground_truth_csv = open(f"{FILE}_ground_truth.csv", mode="r", encoding="utf-8")
ground_truth_read = csv.reader(ground_truth_csv)
answer_csv = open(f"{FILE}_answer.csv", mode="r", encoding="utf-8")
answer_read = csv.reader(answer_csv)

dataset = []
# Initialize
rag = RAG()

for query, ground_truth, answer in zip(question_read, ground_truth_read, answer_read):
    dataset.append(
        {
            "user_input": query[0],
            "retrieved_contexts": rag.get_most_relevant_content(str(query)),
            "response": answer[0],
            "reference": ground_truth[0]
        }
    )

# Evaluation
evaluation_dataset = EvaluationDataset.from_list(dataset)    
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=MODEL))
result = evaluate(
    dataset=evaluation_dataset, 
    metrics=[RougeScore(), StringPresence(), FactualCorrectness()], 
    llm=evaluator_llm
)

print(result)