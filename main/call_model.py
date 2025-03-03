#%%
### PROBABLY NO LONGER NEEDED
# BUT DON'T DELETE AFTER FINAL ONLY
from dotenv import load_dotenv
import numpy as np
from openai import OpenAI
import yaml

from crf import process_input

load_dotenv()

# Load yaml variables
with open("env.yaml", "r") as stream:
    yaml_vars = yaml.safe_load(stream)


def call_model(query: str):
    # Input Prompt
    prompt = yaml_vars['system_prompt'].format(query = query)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that extracts features from natural language prompts."},
        {"role": "user", "content": prompt}
    ]

    # API
    client = OpenAI()
    response = client.chat.completions.create(
        model=yaml_vars['model_name'],
        messages=messages
    )
    
    # Define possible components in the order provided
    all_components = yaml_vars['all_components']
    combined_array = np.zeros(len(all_components))

    content = response.choices[0].message.content.replace("null", "None")
    output = eval(eval(content))

    output = eval(eval(process_input(query)))
            
    for category, items in output.items():
        if isinstance(items, dict):  
            for item, value in items.items():
                if item in all_components:
                    index = all_components.index(item)
                    combined_array[index] = value

    assert combined_array.shape[0]==len(all_components), "error"
    
    return combined_array
