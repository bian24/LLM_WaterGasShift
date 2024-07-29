#%%
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Generate some dummy data
np.random.seed(42)
weights = np.random.uniform(50, 100, 100)  # 100 random weights between 50 and 100 kg
heights = weights * 0.5 + np.random.normal(0, 5, 100)  # height roughly correlated with weight

# Create a DataFrame
data = pd.DataFrame({'Weight': weights, 'Height': heights})

# Split the data into training and testing sets
X = data[['Weight']]
y = data['Height']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
#%%
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="sk-proj-K9d5Gl4z0ShDFUpzoxXAT3BlbkFJWaymTibbyTIge51vjuHB", temperature=0)
# %%
from langchain.agents import tool

@tool
def call_model(weight):
    """
    Returns prediction of a model
    """
    weight = np.array([[weight]])
    height = model.predict(weight)
    return height[0]

tools = [call_model]
# %%
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an assistant that is tasked to predict a person's height 
            in inches based on the given weight in pounds. In the given sentence 
            there will only be a single number that you will need to extract, which is the weight
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

result = list(agent_executor.stream({"input": "what is the person height if he has a weight of 40 "}))