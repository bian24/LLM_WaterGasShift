#%%
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
import yaml

load_dotenv()

# Load yaml variables
with open("env.yaml", "r") as stream:
    yaml_vars = yaml.safe_load(stream)

# Define the input prompt
prompt = yaml_vars['system_prompt']
messages = [
    {"role": "system", "content": "You are a helpful assistant that extracts features from natural language prompts."},
    {"role": "user", "content": prompt}
]

# Define API
client = OpenAI()
response = client.chat.completions.create(
    model=yaml_vars['model_name'],
    messages=messages
)

def call_model(response):
    # Define possible components in the order provided
    all_components = yaml_vars['all_components']
    # Define a single array with zeros
    combined_array = np.zeros(len(all_components))

    max_retries = 100  # Define a limit for retries
    retry_count = 0
    output = None

    # TODO Error Handling
    while retry_count < max_retries:
        try:
            content = response.choices[0].message.content.replace("null", "None")
            output = eval(eval(content))
            retry_count = 0 # reset retry_count
            break  
        except (TypeError, SyntaxError, NameError) as e:
            retry_count += 1
            if retry_count == max_retries:
                return "Max retries reached. Could not evaluate content."
    

    for category, items in output.items():
        if isinstance(items, dict):  
            for item, value in items.items():
                if item in all_components:
                    index = all_components.index(item)
                    combined_array[index] = value

    assert combined_array.shape[0]==len(all_components), "error"
    combined_array = ', '.join(map(str, combined_array))
    
    return combined_array
# %%
print(call_model(response))