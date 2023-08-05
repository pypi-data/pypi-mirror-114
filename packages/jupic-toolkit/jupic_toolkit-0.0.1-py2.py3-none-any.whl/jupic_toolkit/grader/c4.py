from ..jupic import JupIC

def evaluate_c4(
    jupic: JupIC
) -> int:
    '''Evaluate competence 4: Transfer Learning'''

    if not jupic.tl_trained: 
        return 0
        
    if jupic.tl_trained:
        if len(jupic.tl_models) == 1 \
            or len(jupic.tl_epochs) == 1 \
            or len(jupic.tl_learning_rates) == 1: 
                return 1

        if len(jupic.tl_models) > 1 \
            and len(jupic.tl_epochs) > 1 \
            and len(jupic.tl_learning_rates) > 1: 
                return 2
    
    return 0
