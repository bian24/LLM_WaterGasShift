from main.rag import RAG

import csv
import re
import time

# Imports

# TO BE ADJUSTED RAG_FILE PATH
# List of Available Files
# 1. rag_1_script.csv: RAG1
# 2. rag_2_script.csv: RAG2
# 3. rag_12_script.csv: RAG12
FOLDER_PATH = "script"
RAG_VER = "rag_2"

FILE = f"{FOLDER_PATH}/{RAG_VER}"

start_time = time.time()

# Question and Answer CSV
question_csv = open(f"{FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)
ans_csv = open(f"{FILE}_answer.csv", mode="w", encoding="utf-8")
ans_writer = csv.writer(ans_csv)

rag = RAG()
number = 1
for query in question_read:
    answer = re.sub(r'[\*"]', "", rag.generate_answer(str(query)))
    ans_writer.writerow([f"{number}. {answer}"])
    number+=1

ans_csv.close()
print("Writing Answer completed ...")
