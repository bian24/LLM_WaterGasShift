
import torch
import sys
import os
import time
import numpy as np
import pandas as pd
import re
import csv
from huggingface_hub import login,hf_hub_download
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

from main.rag import rag

# Save and Load model 
from transformers import pipeline
question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

context = r"""
Extractive Question Answering is the task of extracting an answer from a text given a question. An example     of a
question answering dataset is the SQuAD dataset, which is entirely based on that task. If you would like to fine-tune
a model on a SQuAD task, you may leverage the examples/pytorch/question-answering/run_squad.py script.
"""

result = question_answerer(question="What is a good example of a question answering dataset?",     context=context)
print(result['answer'])
# RAG

# TO BE ADJUSTED RAG_FILE PATH
# List of Available Files
# 1. rag_1_script.csv: RAG1
# 2. rag_2_script.csv: RAG2
# 3. rag_12_script.csv: RAG12
FOLDER_PATH = "script"
RAG_FILE = "rag_2"
CSV_FILE = f"{FOLDER_PATH}/{RAG_FILE}"


# Q&As per line
qas = []

start_time = time.time()

# Read CSV
question_csv = open(f"{CSV_FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)

# Answer CSV
answer_csv = open(f"{CSV_FILE}_ground_truth.csv", mode="r", encoding="utf-8")
answer_read = csv.reader(answer_csv)


for question, answer in zip(question_read, answer_read):
    # Llama Answer TODO
    llama_answer = "ss"
    # RAG Answer
    rag_answer = re.sub(r'[\*"]', "", rag(str(question)))
    # Ground Truth
    ground_truth = answer
    # Score Comparison
    # TODO LOGIC
    score = 0.5

    # Input per question
    qas.append([question[0], llama_answer, rag_answer, ground_truth[0], score])

# Initialize DataFrame


eval = pd.DataFrame(
    qas,
    columns = [
        'question',
        'llama',
        'rag',
        'ground_truth',
        'score'
    ]
)
eval.to_csv("result.csv")
    
