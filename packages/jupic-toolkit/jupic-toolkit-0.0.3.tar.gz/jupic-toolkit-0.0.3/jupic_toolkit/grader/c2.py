from ..jupic import JupIC

def evaluate_c2(
    jupic: JupIC
) -> int:
    '''Evaluate competence 2: dataset distribution'''
    
    diff = 0
    categories_total = []

    for c in jupic.model_categories:
        c_images = 0    
        
        for ci in jupic.dataset_categories_images:
            for category in ci:
                if c == category:
                    c_images = ci[category]

        categories_total.append(c_images)

    for i in range(len(categories_total) - 1):
        current_total = categories_total[i]
        next_total = categories_total[i + 1]

        diff += abs(current_total - next_total)
        
    if diff > 20: 
        return 0
    if diff > 0 and diff < 20: 
        return 1
    if diff == 0: 
        return 2
        
    return 0