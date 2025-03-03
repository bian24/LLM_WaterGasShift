#%%
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split


#%%

# LLM Declaration
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)# %%

# Tool
from langchain.agents import tool
@tool
def call_model(model, input):
    """
    Returns prediction of a model
    """
    input = np.array([[input]])
    output = model.predict(input)
    return output[0]

tools = [call_model]

# Model
model = pickle.load(open("RF_CO.pkl", "rb"))
print(model.feature_names)

# %%

# Prompt
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an assistant that is tasked to predict the CO conversion 
            in terms of percentage using the given model and inputs
            the input will be in the form of a numpy array, and the output is only a single floating point
            number which is the CO conversion percentage
            """
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent")
    ]
)

llm_with_tools = llm.bind_tools(tools)

#%%
def preprocess_input(input_data):
    try:
        weight = float(input_data)
        return np.array([[weight]])
    except ValueError:
        raise ValueError("Input data must be a number representing the weight.")

#%%
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

agent = (
    {
        "agent": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "input": lambda x: x["input"]

    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = "predict co conversion"
question_input = agent_executor.stream({"input": query})
result = list(question_input)
#%%
# %%
#
