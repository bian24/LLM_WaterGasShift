import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


#IMPORTS
LLM_MODEL = os.getenv("LLM_MODEL")

# Load JSON data
folder = os.path.dirname(os.path.abspath(__file__))


# Extract factual correctness and answer relevance scores
data = pd.read_csv(f"{folder}/run_{LLM_MODEL}.csv")
factual_correctness = data['factual_correctness']
answer_relevance = data['answer_relevancy']
semantic_similarity = data['semantic_similarity']
# Create histogram
plt.figure(figsize=(10, 5))
plt.hist([factual_correctness, answer_relevance, semantic_similarity], bins=np.arange(0, 1.1, 0.1), label=["Factual Correctness", "Answer Relevance", "Semantic Similarity"], alpha=0.7)
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.title(f"Distribution of Factual Correctness and Answer Relevance Scores of {LLM_MODEL}")
plt.legend()
plt.show()
