from ..jupic import JupIC

def evaluate_c10(
    jupic: JupIC
) -> int:
    '''Evalute competence 10: new tests interpretation'''

    success_predictions = 0
    objects_qty = 5

    for i in range(objects_qty):
        if jupic.real_objects[i] == jupic.predicted_objects[i] \
            and jupic.real_objects[i] and jupic.real_objects[i].strip(): 
                success_predictions += 1

    if jupic.predicted_success_times == success_predictions:
        if success_predictions == objects_qty and jupic.predicted_success_interpretation:
                return 2
        else:
            if not jupic.predicted_success_interpretation:
                return 2
    
    return 0
