from ..jupic import JupIC
import json

filename='assessment.json'

def write_json(
    jupic: JupIC,
): 
    '''Writes JSON with JupIC data'''
    
    with open(filename, 'w') as outfile:
        json.dump(jupic, 
            outfile,
            default=lambda o: o.__dict__,  
            indent=4, 
            ensure_ascii=False,
        )