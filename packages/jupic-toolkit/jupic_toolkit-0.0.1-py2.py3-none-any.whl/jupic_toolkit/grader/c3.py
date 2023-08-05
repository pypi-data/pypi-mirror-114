from ..jupic import JupIC

def evaluate_c3(
    jupic: JupIC
) -> int:
    '''Evaluate competence 3: model predictions'''
    
    ratio = jupic.model_correctly_labeled_images / jupic.dataset_total_images

    if ratio < 0.2:
        return 0
    if ratio > 0.2 and ratio < 0.99:
        return 1
    if ratio == 1:
        return 2
        
    return 0
