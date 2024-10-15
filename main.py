from dotenv import load_dotenv
import numpy
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
    assert type(elements_array) == numpy.ndarray, "Not NumPy array"

    # Model Call
    model = pickle.load(open("RF_CO.pkl", "rb"))

    prediction = model.predict([elements_array])

    return prediction[0]

question = "I want to design a catalyst using 5 grams of gold with a CI of 5g, at temperature of 450 with TOS of 4"
print(answer_question(question))

