import json

# returns dict with agents and positions 

def parse_data(filepath):
    with open(filepath) as f:
        data = json.load(f)

    return 