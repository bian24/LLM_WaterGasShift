import sklearn_crfsuite

# Entity lists
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

# Entity-to-column mapping
entity_to_column = {}
column_index = 0

# Add metals, supports, promoters, methods, catalysts, and parameters to the column mapping
for metal in metals:
    entity_to_column[metal.lower()] = column_index
    column_index += 1
for support in supports:
    entity_to_column[support.lower()] = column_index
    column_index += 1
for promoter in promoters:
    entity_to_column[promoter.lower()] = column_index
    column_index += 1
for method in methods:
    entity_to_column[method.lower()] = column_index
    column_index += 1
for catalyst in catalysts:
    entity_to_column[catalyst.lower()] = column_index
    column_index += 1
for parameter in parameters:
    entity_to_column[parameter.lower()] = column_index
    column_index += 1

# Example dataset (list of sentences with (token, label) pairs)
dataset = [
    [('98', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('gold', 'B-METAL'), ('using', 'O'), ('wet-impregnation', 'B-METHOD'), ('process', 'O')],
    [('65', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('platinum', 'B-METAL'), ('on', 'O'), ('titanium', 'B-SUPPORT')],
    [('45', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('ruthenium', 'B-METAL'), ('on', 'O'), ('silicon dioxide', 'B-SUPPORT')],
    [('32', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('rhodium', 'B-METAL'), ('on', 'O'), ('aluminum oxide', 'B-SUPPORT')],
    [('150', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('copper', 'B-METAL'), ('on', 'O'), ('magnesium oxide', 'B-SUPPORT')],
    [('85', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('nickel', 'B-METAL'), ('on', 'O'), ('cerium oxide', 'B-SUPPORT')],
    [('73', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('iridium', 'B-METAL'), ('on', 'O'), ('yttrium oxide', 'B-SUPPORT')],
    [('120', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('palladium', 'B-METAL'), ('on', 'O'), ('magnetite', 'B-SUPPORT')],
    [('50', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('platinum', 'B-METAL'), ('on', 'O'), ('titanium dioxide', 'B-SUPPORT')],
    [('98', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('ruthenium', 'B-METAL'), ('on', 'O'), ('graphene oxide', 'B-SUPPORT')],
    [('75', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('cobalt', 'B-METAL'), ('on', 'O'), ('calcium oxide', 'B-SUPPORT')],
    [('58', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('iridium', 'B-METAL'), ('on', 'O'), ('hydroxyapatite', 'B-SUPPORT')],
    [('82', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('nickel', 'B-METAL'), ('on', 'O'), ('zinc oxide', 'B-SUPPORT')],
    [('130', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('osmium', 'B-METAL'), ('on', 'O'), ('zinc oxide', 'B-SUPPORT')],
    [('110', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('rhodium', 'B-METAL'), ('on', 'O'), ('titanium dioxide', 'B-SUPPORT')],
    [('60', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('palladium', 'B-METAL'), ('on', 'O'), ('silicon dioxide', 'B-SUPPORT')],
    [('40', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('platinum', 'B-METAL'), ('on', 'O'), ('aluminum oxide', 'B-SUPPORT')],
    [('96', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('nickel', 'B-METAL'), ('on', 'O'), ('cerium oxide', 'B-SUPPORT')],
    [('120', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('rhodium', 'B-METAL'), ('on', 'O'), ('magnesium oxide', 'B-SUPPORT')],
    [('150', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('gold', 'B-METAL'), ('on', 'O'), ('magnetite', 'B-SUPPORT')],
    [('70', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('iridium', 'B-METAL'), ('on', 'O'), ('yttrium oxide', 'B-SUPPORT')],
    [('98', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('copper', 'B-METAL'), ('on', 'O'), ('silicon dioxide', 'B-SUPPORT')],
    [('65', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('ruthenium', 'B-METAL'), ('on', 'O'), ('aluminum oxide', 'B-SUPPORT')],
    [('102', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('platinum', 'B-METAL'), ('on', 'O'), ('hydroxyapatite', 'B-SUPPORT')],
    [('110', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('nickel', 'B-METAL'), ('on', 'O'), ('zinc oxide', 'B-SUPPORT')],
    [('85', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('iridium', 'B-METAL'), ('on', 'O'), ('manganese oxide', 'B-SUPPORT')],
    [('120', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('osmium', 'B-METAL'), ('on', 'O'), ('hydroxyapatite', 'B-SUPPORT')],
    [('60', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('rhodium', 'B-METAL'), ('on', 'O'), ('calcium oxide', 'B-SUPPORT')],
    [('75', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('ruthenium', 'B-METAL'), ('on', 'O'), ('magnesium oxide', 'B-SUPPORT')],
    [('55', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('cobalt', 'B-METAL'), ('on', 'O'), ('graphene oxide', 'B-SUPPORT')],
    [('65', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('platinum', 'B-METAL'), ('on', 'O'), ('titanium dioxide', 'B-SUPPORT')],
    [('50', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('nickel', 'B-METAL'), ('on', 'O'), ('silicon dioxide', 'B-SUPPORT')],
    [('90', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('iridium', 'B-METAL'), ('on', 'O'), ('titanium oxide', 'B-SUPPORT')],
    [('40', 'B-QUANTITY'), ('g', 'B-UNIT'), ('of', 'O'), ('palladium', 'B-METAL'), ('on', 'O'), ('titanium dioxide', 'B-SUPPORT')]
]


def extract_features(sentence, i):
    """
    Map each feature in a prompt to its categorical type
    
    Args:
        - sentence (str) prompt that depicts the experiment
        - i (int) index position

    Returns:
        - features (list)
    """
    token = sentence[i][0]
    features = {
        'word': token,
        'is_upper': token.isupper(),
        'is_title': token.istitle(),
        'is_digit': token.isdigit(),
    }
    if i > 0:
        features['prev_word'] = sentence[i-1][0]
    else:
        features['BOS'] = True 
    
    if i < len(sentence) - 1:
        features['next_word'] = sentence[i+1][0]
    else:
        features['EOS'] = True 
    return features


def prepare_data(data):
    """
    Annotate datasets features to its corresponding labels
    
    Args:
        - data(list)
    
    Returns:
        - X(list) segmented features of a given prompt
        - y(list) label of each corresponding feature to X
    """
    X, y = [], []
    for sentence in data:
        X.append([extract_features(sentence, i) for i in range(len(sentence))])
        y.append([label for _, label in sentence])
    
    return X, y


# Train CRF Model
X_train, y_train = prepare_data(dataset)
crf = sklearn_crfsuite.CRF(
    algorithm='lbfgs',
    c1=0.1,  # L1 regularization
    c2=0.1,  # L2 regularization
    max_iterations=100,
    all_possible_transitions=True
)
crf.fit(X_train, y_train)


def process_input(input_prompt):
    """
    Process Input and give a 98 x 1 resulting vector output of each feature mentioned
    
    Args:
        - input_prompt(str) prompt that depict the experiment
     
    Returns:
        - vector output (list) 98 x 1 list that characterizes the experiment of features"""
    # Preprocess
    tokens = input_prompt.split()
    tokens = [' '.join(token.split('-')) for token in tokens] 
    sentence = [(token, 'O') for token in tokens]  
    X_input = [extract_features(sentence, i) for i in range(len(sentence))]
    
    # Prediction
    y_pred = crf.predict([X_input])[0]  #
    
    # Initialize a 98x1 vector (all zeros initially)
    vector = [0] * 98
    quantity = None
    for token, label in zip(tokens, y_pred):
        if label == 'B-QUANTITY' and token.isdigit():
            quantity = float(token)  
            
        elif label == 'B-METAL' and token.lower() in entity_to_column:
            # Map quantity to the corresponding metal column
            column = entity_to_column[token.lower()]
            if quantity:
                vector[column] = quantity 
            else:
                vector[column] = 1  
        
        elif label == 'B-PROMOTER' and token.lower() in entity_to_column:
            # Map quantity to the corresponding promoter column
            column = entity_to_column[token.lower()]
            if quantity:
                vector[column] = quantity  
            else:
                vector[column] = 1  
        
        elif label == 'B-SUPPORT' and token.lower() in entity_to_column:
            # Map quantity to the corresponding support column
            column = entity_to_column[token.lower()]
            if quantity:
                vector[column] = quantity  
            else:
                vector[column] = 1 
        
        elif label == 'B-METHOD' and token.lower() in entity_to_column:
            # Set process column to 1 if a process is mentioned
            column = entity_to_column[token.lower()]
            vector[column] = 1
    
    return vector
