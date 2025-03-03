from dotenv import load_dotenv
import pickle
import os

from crf import process_input

load_dotenv()


# Imports
MODEL = os.getenv("ML_MODEL")
XGB_MODEL = os.getenv("XGB_MODEL")


class RAG5:
    def __init__(self):
        self.model = pickle.load(open(XGB_MODEL, "rb"))


    def generate_answer(self, query):
        """
        Utilise existing xgboost model to predict CO conversion
        """
        elements_array = process_input(query)
        prediction = self.model.predict([elements_array])

        return prediction[0]
