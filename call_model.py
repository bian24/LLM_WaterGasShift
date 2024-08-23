#%%
import numpy as np
import json
import openai

# Define your API key
openai.api_key = 'sk-proj-K9d5Gl4z0ShDFUpzoxXAT3BlbkFJWaymTibbyTIge51vjuHB'

# Define the input prompt
messages = [
    {"role": "system", "content": "You are a helpful assistant that extracts features from natural language prompts."},
    {"role": "user", "content": """
    Extract the features related to metals, promoters, oxides, and process conditions from the following sentence:
    "I want to design a catalyst using 3 grams of gold with a chlorination impregnation promoter of 5g, calcined at 450 degrees Celsius for 4 hours, and the reaction temperature set to 350 degrees Celsius."
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
    }
]

# Make the API call
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=150,
    temperature=0
)

# Extract the output
output = response['choices'][0]['message']['content'].strip()

# Convert the output to a dictionary
extracted_features = json.loads(output)

print(extracted_features)
# %%
# Define the possible components for each category in the order provided
all_components = [
    'platinum', 'gold', 'ruthenium', 'rhodium', 'iridium', 'copper', 'palladium',
    'incipient wetness impregnation', 'wet impregnation', 'chlorination impregnation',
    'sol-gel process', 'supercritical drying', 'co-precipitation', 'hydrothermal deposition',
    'ultrasound-assisted impregnation', 'surface characterization techniques',
    'flame spray pyrolysis', 'mechanochemical', 'deposition precipitation',
    'aluminum oxide', 'magnesium oxide', 'cerium oxide', 'titanium dioxide', 'zeolite',
    'manganese oxide', 'yttrium oxide', 'zirconium dioxide', 'hydroxyapatite',
    'activated carbon composite', 'terbium oxide', 'hafnium dioxide', 'lanthanum oxide',
    'cobalt oxide', 'thorium dioxide', 'silicon dioxide', 'iron(III) oxide',
    'samarium oxide', 'gadolinium oxide', 'ytterbium oxide', 'calcium oxide', 'nickel oxide',
    'chromium(III) oxide', 'holmium oxide', 'neodymium oxide', 'thulium oxide',
    'erbium oxide', 'yttria-stabilized zirconia',
    'calcination temperature', 'calcination time', 'reaction temperature',
    'hydrogen volume percentage', 'oxygen volume percentage', 'carbon monoxide volume percentage',
    'water volume percentage', 'carbon dioxide volume percentage', 'methane volume percentage',
    'time on stream', 'weight hourly space velocity'
]

# Define the input dictionary
input_dict = {
    'metals': {'gold': 3.0},
    'promoters': {'chlorination impregnation': 5.0},
    'oxides': {},
    'process_conditions': {'calcination temperature': 450.0, 'calcination time': 4.0, 'reaction temperature': 350.0},
    'conversion': None
}

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

# Apply the update
update_array_from_dict(all_components, input_dict)

combined_array = ', '.join(map(str, combined_array))

# Print the result
print('Combined Array:', combined_array)

# %%
