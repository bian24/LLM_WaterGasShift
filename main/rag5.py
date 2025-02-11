from dotenv import load_dotenv
import pickle
import os

load_dotenv()

from crf import process_input

# Imports
MODEL = os.getenv("ML_MODEL")


def rag_5(question: str) -> int:
    """
    Calls XGBoost model to calculate CO conversion
    
    Args:
        - question(str) prompt that depict the experiment
    Returns:
        - (int) CO conversion in percentage of said experiment
    """
    elements_array = process_input(question)
    # Model Used
    model = pickle.load(open("RF_CO.pkl", "rb"))

    prediction = model.predict([elements_array])

    return prediction[0]

# change this to try out different question, if it says assertion error try until it works
question = "i want to design a catalyst using 0.87 grams of gold with 5g of aluminum oxide on a calcination temperature of 100 degrees celcius"