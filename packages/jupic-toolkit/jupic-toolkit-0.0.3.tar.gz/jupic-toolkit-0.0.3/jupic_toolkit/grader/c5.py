from ..jupic import JupIC

def evaluate_c5(
    jupic: JupIC
) -> int:
    '''Evaluate competence 5: Fine-Tuning'''

    if not jupic.ft_unfreezed: 
        return 0

    if jupic.ft_unfreezed:
        if jupic.ft_trained and jupic.ft_learning_rate_found: 
            return 2 

        return 1

    return 0
