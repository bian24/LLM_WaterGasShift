import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


# IMPORTS
LLM_MODEL = os.getenv("LLM_MODEL")
RAG_VER = "DB_2"
RAG = ""

# Load data
folder = os.path.dirname(os.path.abspath(__file__))

# Extract factual correctness and answer relevance scoresz

data = pd.read_csv(f"{folder}/run_{RAG_VER}_{LLM_MODEL}.csv")
data_points = {
    'factual_correctness':  pd.Series(data['factual_correctness']),
    'answer_relevancy': pd.Series(data['answer_relevancy']),
    'semantic_similarity':  pd.Series(data['semantic_similarity'])
}


for metric_name, metric_values in data_points.items():
    plt.figure(figsize=(20, 6))
    plt.bar(metric_values.index, metric_values.values)
    plt.axhline(y=0.5, color='red', linestyle='--', label='Level 0.5')
    plt.axhline(y=metric_values.mean(), color='green', linestyle='--', label=f'Average: {metric_values.mean():.2f}')
    plt.xlabel("Prompt")
    plt.ylabel("Value")
    plt.title(f"{metric_name.capitalize()} {LLM_MODEL} {RAG} on {RAG_VER}")
    plt.legend()
    plt.show()

