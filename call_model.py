#%%
from dotenv import load_dotenv
import numpy as np
import json
from openai import OpenAI
import yaml

load_dotenv()

# Load yaml variables
with open("env.yaml", "r") as stream:
    yaml_vars = yaml.safe_load(stream)

# Define the input prompt
prompt = """
    Extract the features related to metals, promoters, oxides, and process conditions from the following sentence:
    "I want to design a catalyst using 3 grams of aluminium with a chlorination impregnation promoter of 5g, calcined at 450 degrees Celsius for 4 hours, and the reaction temperature set to 350 degrees Celsius."
    Classify them as follows:
    - Metals: platinum, gold, ruthenium, rhodium, iridium, copper, palladium, cerium, cobalt, magnesium, iron, manganese, zirconium, potassium, nickel, calcium, cesium, vanadium, rubidium, yttrium, sodium, lanthanum, gadolinium, ytterbium, zinc, rhenium, strontium.
    - Promoters: incipient wetness impregnation, wet impregnation, chlorination impregnation, sol-gel process, supercritical drying, co-precipitation, hydrothermal deposition, ultrasound-assisted impregnation, surface characterization techniques, flame spray pyrolysis, mechanochemical, deposition precipitation.
    - Oxides: aluminum oxide, magnesium oxide, cerium oxide, titanium dioxide, zeolite, manganese oxide, yttrium oxide, zirconium dioxide, hydroxyapatite, activated carbon composite, terbium oxide, hafnium dioxide, lanthanum oxide, cobalt oxide, thorium dioxide, silicon dioxide, iron(III) oxide, samarium oxide, gadolinium oxide, ytterbium oxide, calcium oxide, nickel oxide, chromium(III) oxide, holmium oxide, neodymium oxide, thulium oxide, erbium oxide, yttria-stabilized zirconia.
    - Process Conditions: calcination temperature (in degrees Celsius), calcination time (in hours), reaction temperature (in degrees Celsius), hydrogen volume percentage, oxygen volume percentage, carbon monoxide volume percentage, water volume percentage, carbon dioxide volume percentage, methane volume percentage, time on stream (in minutes), weight hourly space velocity (in mg.min/ml).
    {
  "metals": {"type of metal such as platinum": "its weight as a floating-point number"},
  "promoters": {"type promoters mentioned": "their weight as a floating-point number"},
  "oxides": {"type of oxides mentioned": "their weight as a floating-point number"},
  "process_conditions": {"type of process conditions mentioned": "their values as floating-point numbers without units"},
  "conversion": null
    }

    Ensure that all numeric values are returned as floating-point numbers without any units such as 'grams' or 'degrees'.
    """

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

# Extract the output
output = response.choices[0].message.content

# Convert the output to a dictionary
print(output)
# %%
# Define the possible components for each category in the order provided
all_components = yaml_vars['all_components']
print(all_components)
# add assertion confirmation for error handling

# Define the input dictionary
input_dict = output

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
update_array_from_dict(all_components, input_dict)
combined_array = ', '.join(map(str, combined_array))

# Assertion 1. Compare input with array output


print('Combined Array:', combined_array)

# %%
assert 1==2, "error"