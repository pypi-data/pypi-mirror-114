from ..jupic import JupIC

def evaluate_c9(
    jupic: JupIC
) -> int:
    '''Evalute competence 9: new tests'''

    tests = 0
   
    for o in jupic.predicted_objects:
        if o and o.strip(): 
            tests += 1

    if tests == 0:
        return 0
    if tests > 0 and tests < 3:
        return 1
    if tests > 2:
        return 2

    return 0