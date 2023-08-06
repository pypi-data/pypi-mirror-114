from ..jupic import JupIC

def evaluate_c6(
    jupic: JupIC
) -> int:
    '''Evaluate competence 6: accuracy'''

    if jupic.accuracy_analysis:
        return evaluate_accuracy_success_interpretation(jupic)
    else:
        return evaluate_accuracy_fail_interpretation(jupic)


def evaluate_accuracy_success_interpretation(
    jupic: JupIC
) -> int:
    '''Evalute success accuracy interpretation answer'''

    for c in jupic.model_categories:
        c_accuracy = 0.0
        
        for ac in jupic.accuracy_categories:
            for category in ac: 
                if c == category:
                    c_accuracy = ac[category]
        
        if c_accuracy < 0.9: 
            return 0

    if jupic.accuracy_interpretation: 
        return 2
    else: 
        return 1


def evaluate_accuracy_fail_interpretation(
    jupic: JupIC
) -> int:
    '''Evalute fail accuracy interpretation answer'''

    if jupic.accuracy_interpretation: 
        return 0
        
    if set(jupic.accuracy_analysis_categories) == set(get_low_accuracy_categories(jupic)):
        if jupic.accuracy_interpretation:        
            return 1
        else:
            return 2

    return 0


def get_low_accuracy_categories(
    jupic: JupIC
) -> list:
    '''Returns categories below 90% threshold accuracy'''

    low_accuracy_categories = []

    for c in jupic.model_categories:
        c_accuracy = 0.0
        
        for ac in jupic.accuracy_categories:
            for category in ac: 
                if c == category:
                    c_accuracy = ac[category]

        if c_accuracy < 0.9: 
            low_accuracy_categories.append(c)

    return low_accuracy_categories  