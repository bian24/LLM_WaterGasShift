import os
import pickle

from crf import CRF

XGB_MODEL = os.getenv("XGB_MODEL")


class rag3:
    def __init__(self):
        self.crf = CRF()
        self.model = pickle.load(open(XGB_MODEL, "rb"))

    def generate_answer(self, query):
        """
        Generate CO Conversion based on Chattoraj et.al, 2022
        Improving Theory-Guided Machine Learning in Water-Gas Shift
        """
        # Feature Extraction
        features_extract = self.crf.process_input(query)
        print(features_extract)
        # CO Conversion
        answer = self.model.predict([features_extract])[0]

        return answer