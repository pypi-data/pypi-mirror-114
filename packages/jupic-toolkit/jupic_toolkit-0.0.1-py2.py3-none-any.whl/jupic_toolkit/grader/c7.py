from ..jupic import JupIC

def evaluate_c7(
    jupic: JupIC
) -> int:
    '''Evalute competence 7: confusion matrix'''

    mislabeled_identified = 0

    for index, mislabeled in enumerate(jupic.confusion_matrix_mislabeled):
        for c in jupic.model_categories:
            for category in mislabeled: 
                if category == c \
                    and set(jupic.confusion_matrix_mislabeled[index][c]) == \
                        set(jupic.confusion_matrix_mislabeled_real[index][c]):
                            mislabeled_identified += 1

    if mislabeled_identified == len(jupic.model_categories):
        has_mislabel = False

        for c in jupic.confusion_matrix_mislabeled_real:
           for mislabeled in c:
               if len(mislabeled) > 0:
                   has_mislabel = True

        if jupic.confusion_matrix_interpretation:
            if has_mislabel:
                return 1
            else:
                return 2
        else:
            if has_mislabel:
                return 2
            else:
                return 1
    
    return 0
