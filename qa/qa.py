import csv
import os
import re
import time

from main.rag import RAG
from main.base_llm import BaseLLM


# Imports

# TO BE ADJUSTED DB PATH
# List of Available Files
# 1. DB_1: Database of PDF-1
# 2. DB_2: Database of PDF-2
# 3. DB_12: Database of PDF-12
FOLDER_PATH = "script"
DB = "DB_2"
FILE = f"{FOLDER_PATH}/{DB}"

# For Base LLM Testing
# 1. gpt-4o-mini
# 2. llama3.2
# For RAG Testing
# 1. gpt-4o-mini_rag
# 2. llama3.2 rag

LLM_MODEL = "gpt-4o-mini_rag"


# Question and Answer CSV
question_csv = open(f"{FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)
ans_csv = open(f"{FILE}_answer_{LLM_MODEL}.csv", mode="w", encoding="utf-8")
ans_writer = csv.writer(ans_csv)



if "rag" in LLM_MODEL:
    model = LLM_MODEL.replace("_rag", "")
    rag = RAG(model)
    number = 1
    for query in question_read:
        answer = re.sub(r'[\*"]', "", rag.generate_answer(str(query)))
        ans_writer.writerow([f"{number}. {answer}"])
        number+=1
else:
    basellm = BaseLLM()
    number = 1
    for query in question_read:
        answer = re.sub(r'[\*"]', "", basellm.generate_answer(str(query)))
        ans_writer.writerow([f"{number}. {answer}"])
        number+=1

ans_csv.close()
print("Writing Answer completed ...")
