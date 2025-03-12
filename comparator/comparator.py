import csv
import os
from langchain_openai import ChatOpenAI
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import ResponseRelevancy, FactualCorrectness, Faithfulness

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

rag = RAG()

# Question and Ground Truth CSV
question_csv = open(f"{FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)
ground_truth_csv = open(f"{FILE}_ground_truth.csv", mode="r", encoding="utf-8")
ground_truth_read = csv.reader(ground_truth_csv)
answer_csv = open(f"{FILE}_answer.csv", mode="r", encoding="utf-8")
answer_read = csv.reader(answer_csv)


dataset = []

for query, ground_truth, answer in zip(question_read, ground_truth_read, answer_read):
    dataset.append(
        {
            "user_input": query[0],
            "retrieved_contexts": [(''.join(rag.get_most_relevant_content(str(query[0]))))],
            "response": answer[0],
            "reference": ground_truth[0]
        }
    )

# Evaluation
evaluation_dataset = EvaluationDataset.from_list(dataset)    
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=MODEL))
result = evaluate(
    dataset=evaluation_dataset, 
    metrics=[FactualCorrectness(), Faithfulness(), ResponseRelevancy()], 
    llm=evaluator_llm
)
result.upload()