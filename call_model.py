#%%
from dotenv import load_dotenv
import numpy as np
import json
from openai import OpenAI
import yaml
import re

load_dotenv()

# Load yaml variables
with open("env.yaml", "r") as stream:
    yaml_vars = yaml.safe_load(stream)



# Define the input prompt
prompt = yaml_vars['system_prompt'] # combination of system prompt
messages = [
    {"role": "system", "content": "You are a helpful assistant that extracts features from natural language prompts."},
    {"role": "user", "content": prompt}
]

# Make the API call
client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=messages
)

# Extract and convert the output to a dictionary
output = response.choices[0].message.content.replace("null", "None")
output = re.sub('\s+', ' ', output)
dict_output = eval(output)

# TODO
# assume that the output is already dict, but still need to fix
output = {"Metals": {"aluminium": 3.0}, "Promoters": {"chlorination impregnation": 5.0}, "Oxides": {}, "Process Conditions": {"calcination_temperature": 450.0, "calcination_time": 4.0, "reaction_temperature": 350.0}}

# %%
# Define the possible components for each category in the order provided
all_components = yaml_vars['all_components']

# Initialize a single array with zeros
combined_array = np.zeros(len(all_components))

# Update the array based on the input dictionary
def update_array_from_dict(component_list, dictionary):
    for category, items in dictionary.items():
        if isinstance(items, dict):  # Ensure items is a dictionary
            for item, value in items.items():
                if item in component_list:
                    index = component_list.index(item)
                    combined_array[index] = value

## add something that can verify the output array, assertion comparing input prompt with array output
update_array_from_dict(all_components, output)

assert combined_array.shape[0]==len(all_components), "error"
combined_array = ', '.join(map(str, combined_array))
print(combined_array)
