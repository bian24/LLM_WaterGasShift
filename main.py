### prompt question
### using lc_agents to call the tool in call_model
'''
main.py (question) ---> 
call_model.py (question) ---> array of inputs
lc_agents.py (array of inputs) ---> output
'''

from dotenv import load_dotenv
import numpy
import os
import pickle

load_dotenv

from call_model import call_model

question = "I want to design a catalyst using 5 grams of gold with a CI of 5g, at temperature of 450 with TOS of 4"
# numpy array of dimensions of the model
elements_array = call_model(question)
assert type(elements_array) == numpy.ndarray, "Not NumPy array"

# Model Call
model = pickle.load(open("RF_CO.pkl", "rb"))

def predict(elements):
    prediction = model.predict([elements])

    return prediction

print(predict(elements_array))

