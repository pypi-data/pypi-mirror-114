from ..jupic import JupIC

def evaluate_c8(
    jupic: JupIC
) -> int:
    '''Evalute competence 8: performance tuning'''

    if jupic.performance_tuning == 'Não':
        return 0

    if jupic.performance_tuning == 'Sim, uma vez, mudando o que? Melhorou?' \
        or jupic.performance_tuning == 'Sim, várias vezes, mudando o que? Melhorou?':
            
            if jupic.performance_tuning_text and jupic.performance_tuning_text.strip():
                return 2
            if not jupic.performance_tuning_text and jupic.performance_tuning_text.strip():
                return 1

    return 0
