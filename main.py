from dotenv import load_dotenv
import numpy as np
import os
import pickle

load_dotenv

from call_model import call_model


def answer_question(question: str) -> int:
    """
    Return the answer to the question
    
    Args:
        - question(str)
    Returns:
        - int CO conversion of said experiment
    """
    # numpy array of dimensions of the model
    elements_array = call_model(question)
    print(elements_array)
    assert type(elements_array) == np.ndarray, "Not NumPy array"

    # Model Call
    model = pickle.load(open("RF_CO.pkl", "rb"))

    prediction = model.predict([elements_array])

    return prediction[0]

# change this to try out different question, if it says assertion error try until it works
question = "i want to design a catalyst using 0.87 grams of gold calcination temperature of 100 degrees celcius"
print(answer_question(question))
