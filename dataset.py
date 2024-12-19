import random

# Define entity lists
metals = ['Platinum', 'Gold', 'Ruthenium', 'Rhodium', 'Iridium', 'Copper', 'Palladium', 'Nickel', 'Osmium', 'Rhenium']
supports = [
    'Aluminum Oxide', 'Magnesium Oxide', 'Cerium Oxide', 'Titanium Dioxide', 
    'Titanium Dioxide P25', 'Manganese Oxide', 'Yttrium Oxide', 'Zirconium Oxide', 
    'Hydroxyapatite', 'Amorphous Calcium Carbonate', 'Hafnium Oxide', 
    'Lanthanum Oxide', 'Cobalt Oxide', 'Silicon Dioxide', 'Zinc Oxide', 
    'Magnetite (Iron(II,III) Oxide)', 'Hematite (Iron(III) Oxide)', 
    'Calcium Oxide', 'Ruthenium Dioxide', 'Gallium Oxide', 'Uranium Trioxide', 
    'Triuranium Octoxide', 'Chromium(III) Oxide', 'Manganese Dioxide', 
    'Graphene Oxide', 'Alpha Molybdenum Carbide', 'Molybdenum Nitride'
]
promoters = [
    'Lithium', 'Cerium', 'Cobalt', 'Iron', 'Manganese', 'Zirconium', 'Potassium', 
    'Nickel', 'Cesium', 'Rubidium', 'Yttrium', 'Sodium', 'Lanthanum', 'Gadolinium', 
    'Praseodymium', 'Zinc'
]
methods = [
    'Impregnation with Inverse Water', 'Wet Impregnation', 'Chemical Impregnation', 
    'Solid Impregnation', 'Sol-Gel Process', 'Co-precipitation', 'High-Density Plasma', 
    'Ultrasonic Gelation Coating', 'Solid State Combustion', 'Flame Spray Pyrolysis', 
    'Mechanochemical Synthesis', 'Dip Coating', 'Ultraviolet Curing', 'Thermal Decomposition', 
    'Self-Combustion Method', 'Direct Ammonia Synthesis', 'Hydrothermal Synthesis', 
    'Thermal Co-precipitation', 'Direct Current Plasma', 'Low-Pressure Reduction Deposition', 
    'Chemical Vapor Deposition', 'Rapid Solidification of Thermal Deposition', 
    'Milling Process', 'Hydrothermal Method', 'Nanocasting', 'Evaporation-Induced Self-Assembly', 
    'Chemical Adsorption', 'Chemical Deposition', 'Ultrasonic Spray Method', 'Plasma Treatment', 
    'Acoustic Emission Heating', 'Acid Precipitation'
]
catalysts = [
    'Krypton', 'Carbon Monoxide', 'Water', 'Carbon Dioxide', 'Hydrogen', 
    'Oxygen', 'Methane', 'Nitrogen', 'Helium', 'Argon'
]
parameters = ['temperature', 'TOS', 'W/F']

# Units
mass_unit = ['g']
temperature_unit = ['°C']
volume_unit = ['mL']
concentration_unit = ['vol.%']
time_unit = ['h']
flow_rate_unit = ['mg.min/mL']

# Define sentence templates
templates = [
    "{QUANTITY} {MASS_UNIT} of {METAL} on {SUPPORT} was prepared using {METHOD} at {QUANTITY} {TEMPERATURE_UNIT} temperature.",
    "{METHOD} was employed to prepare {QUANTITY} {MASS_UNIT} of {METAL}-based catalyst with {QUANTITY} {MASS_UNIT} of {SUPPORT}.",
    "The catalyst containing {QUANTITY} {MASS_UNIT} of {METAL} on {SUPPORT} was synthesized via {METHOD}.",
    "At {QUANTITY} {MASS_UNIT} temperature, {QUANTITY} {MASS_UNIT} of {METAL} on {SUPPORT} was reacted.",
    "A catalyst system comprising {QUANTITY} {MASS_UNIT} of {PROMOTER} and {QUANTITY} {MASS_UNIT} of {SUPPORT} was prepared using {METHOD}.",
    "{QUANTITY} {CONCENTRATION_UNIT} of {CATALYST} with {QUANTITY} {MASS_UNIT} of {PROMOTER} was reacted at a flow rate of {QUANTITY} {FLOW_RATE_UNIT}.",
    "The reaction used {QUANTITY} {MASS_UNIT} of {METAL}, {QUANTITY} {MASS_UNIT} of {PROMOTER}, and was carried out at {QUANTITY} {FLOW_RATE_UNIT} W/F."
]

# Function to generate a synthetic sentence and its annotation
def generate_synthetic_data(num_sentences):
    data = []

    for _ in range(num_sentences):
        template = random.choice(templates)
        
        # Dynamically select entities based on template requirements
        metal = random.choice(metals)
        support = random.choice(supports)
        promoter = random.choice(promoters)
        method = random.choice(methods)
        catalyst = random.choice(catalysts)
        parameter = random.choice(parameters)
        
        # Random quantity
        quantity = random.randint(1, 100)
        
        # Fill in placeholders dynamically based on the template
        sentence = template.format(
            METAL=metal,
            SUPPORT=support,
            PROMOTER=promoter,
            METHOD=method,
            CATALYST=catalyst,
            PARAMETER=parameter,
            QUANTITY=quantity,
            MASS_UNIT=mass_unit[0],
            TEMPERATURE_UNIT=temperature_unit[0],
            VOLUME_UNIT=volume_unit[0],
            CONCENTRATION_UNIT=concentration_unit[0],
            TIME_UNIT=time_unit[0],
            FLOW_RATE_UNIT=flow_rate_unit[0]
        )
        
        annotated_sentence = annotate_sentence(sentence)
        data.append(annotated_sentence)

    return data

# Function to annotate the sentence
def annotate_sentence(sentence):
    tokens = sentence.split()
    annotated_tokens = []

    for token in tokens:
        if token.lower() in metals:
            annotated_tokens.append((token, 'B-METAL'))
        elif token.lower() in supports:
            annotated_tokens.append((token, 'B-SUPPORT'))
        elif token.lower() in promoters:
            annotated_tokens.append((token, 'B-PROMOTER'))
        elif token.lower() in methods:
            annotated_tokens.append((token, 'B-METHOD'))
        elif token.lower() in catalysts:
            annotated_tokens.append((token, 'B-CATALYST'))
        elif token.lower() in parameters:
            annotated_tokens.append((token, 'B-PARAMETER'))
        elif token.isdigit():
            annotated_tokens.append((token, 'B-QUANTITY'))
        elif any(unit in token for unit in mass_unit + temperature_unit + volume_unit + concentration_unit):
            annotated_tokens.append((token, 'B-UNIT'))
        else:
            annotated_tokens.append((token, 'O'))  # Default to outside

    return annotated_tokens

# Generate synthetic data
synthetic_data = generate_synthetic_data(num_sentences=5)
print(synthetic_data)
