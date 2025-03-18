import json
import matplotlib.pyplot as plt
import numpy as np
import os


#IMPORTS
LLM_MODEL = os.getenv("LLM_MODEL")

# Load JSON data
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
path = f"{parent_dir}/run/{LLM_MODEL}_run.json"

with open(path, "r") as file:
    data = json.load(file)

# Extract factual correctness and answer relevance scores
factual_correctness, answer_relevance, semantic_similarity = [], [], []

for entry in data['factual_correctness']:
    factual_correctness.append(entry['metric_output'])
for entry in data['answer_relevancy']:
    answer_relevance.append(entry['metric_output'])
for entry in data['semantic_similarity']:
    semantic_similarity.append(entry['semantic_similarity'])


# Create histogram
plt.figure(figsize=(10, 5))
plt.hist([factual_correctness, answer_relevance, semantic_similarity], bins=np.arange(0, 1.1, 0.1), label=["Factual Correctness", "Answer Relevance", "Semantic Similarity"], alpha=0.7)
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.title(f"Distribution of Factual Correctness and Answer Relevance Scores of {LLM_MODEL}")
plt.legend()
plt.show()
