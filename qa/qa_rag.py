from main.rag import rag

import csv
import re
import time

# Imports

# TO BE ADJUSTED RAG_FILE PATH
# List of Available Files
# 1. rag_1_script.csv: RAG1
# 2. rag_2_script.csv: RAG2
# 3. rag_12_script.csv: RAG12
RAG_FILE = "rag_2"
FOLDER_PATH = "script"
CSV_FILE = f"{FOLDER_PATH}/{RAG_FILE}"

start_time = time.time()

# Read CSV
question_csv = open(f"{CSV_FILE}.csv", mode="r", encoding="utf-8")
question_read = csv.reader(question_csv)

# Answer CSV
ans_csv = open(f"{CSV_FILE}_answer.csv", mode="w", encoding="utf-8")
ans_writer = csv.writer(ans_csv)

number = 1
for question in question_read:
    answer = re.sub(r'[\*"]', "", rag(str(question)))
    ans_writer.writerow([f"{number}. {answer}"])
    ans_writer.writerow([])
    number+=1

end_time = time.time()
ans_writer.writerow(["-"*100])
ans_writer.writerow([f"Total time is {round(end_time-start_time,2)} second"])
ans_csv.close()
