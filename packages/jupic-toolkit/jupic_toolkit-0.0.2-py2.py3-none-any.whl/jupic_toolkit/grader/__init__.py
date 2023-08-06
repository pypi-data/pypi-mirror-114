from ..jupic import JupIC
from .c1 import evaluate_c1
from .c2 import evaluate_c2
from .c3 import evaluate_c3
from .c4 import evaluate_c4
from .c5 import evaluate_c5
from .c6 import evaluate_c6
from .c7 import evaluate_c7
from .c8 import evaluate_c8
from .c9 import evaluate_c9
from .c10 import evaluate_c10
import math

def evaluate(
    jupic: JupIC
) -> dict:
    '''Evaluate JupIC data'''

    res = {}
    total_score = 0

    # C1
    score = evaluate_c1(jupic)
    res['category_images'] = score
    total_score += score
    # C2
    score = evaluate_c2(jupic)
    res['dataset_distribution'] = score
    total_score += score
    # C3
    score = evaluate_c3(jupic)
    res['model_predictions'] = score
    total_score += score
    # C4
    score = evaluate_c4(jupic)
    res['transfer_learning'] = score
    total_score += score
    # C5
    score = evaluate_c5(jupic)
    res['fine_tuning'] = score
    total_score += score
    # C6
    score = evaluate_c6(jupic)
    res['accuracy'] = score 
    total_score += score
    # C7
    score = evaluate_c7(jupic)
    res['confusion_matrix'] = score
    total_score += score
    # C8
    score = evaluate_c8(jupic)
    res['performance_tuning'] = score 
    total_score += score
    # C9
    score = evaluate_c9(jupic)
    res['new_tests'] = score 
    total_score += score
    # C10
    score = evaluate_c10(jupic)
    res['new_tests_interpretation'] = score 
    total_score += score
    # Total score
    res['total_score'] = math.floor(total_score / 2) 

    return res