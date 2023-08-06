from .jupic import JupIC
from .grader import evaluate
from .json import write_json
from .ninja_robot import display

__ipynb = {}
##### Model
__ipynb['model_categories'] = ['Aroeira','Jeriva','Pitangueira','Embauba', 'Mulungu', 'Capororoca']
__ipynb['model_correctly_labeled_images'] = 100
###### Dataset
__ipynb['dataset_categories_images'] = [
    { 'Aroeira': 20 }, 
    { 'Capororoca': 20 }, 
    { 'Embauba': 20 }, 
    { 'Jeriva': 20 }, 
    { 'Mulungu': 20 }, 
    { 'Pitangueira': 20 }
]
__ipynb['dataset_total_images'] = 100
###### Transfer Learning
__ipynb['tl_models'] = ["resnet50", "resnet32"]
__ipynb['tl_epochs'] = [1, 2]
__ipynb['tl_learning_rates'] = [0e-1, 0e-2]
__ipynb['tl_trained'] = True
##### Fine Tuning
__ipynb['ft_unfreezed'] = True
__ipynb['ft_learning_rate_found'] = True
__ipynb['ft_trained'] = True
##### Accuracy
__ipynb['accuracy_categories'] = [
    { 'Aroeira': 0.1 }, 
    { 'Capororoca': 0.2 }, 
    { 'Embauba': 0.3 }, 
    { 'Jeriva': 0.4 }, 
    { 'Mulungu': 0.5 }, 
    { 'Pitangueira': 0.6 }
]
__ipynb['accuracy_analysis'] = "Falso"
__ipynb['accuracy_analysis_categories'] = ["Aroeira", "Capororoca", "Embauba", "Jeriva", "Mulungu", "Pitangueira"]
__ipynb['accuracy_interpretation'] = "Falso"
##### Confusion matrix
__ipynb['confusion_matrix_mislabeled_real'] = [{'Pitangueira': ['Capororoca', 'Aroeira', 'Embauba', 'Mulungu']}, {'Jeriva': []}, {'Capororoca': ['Jeriva', 'Aroeira']}, {'Mulungu': []}, {'Embauba': []}, {'Aroeira': ['Pitangueira', 'Embauba', 'Jeriva', 'Mulungu']}]
__ipynb['confusion_matrix_mislabeled'] = [{'Pitangueira': ['Aroeira', 'Capororoca', 'Embauba', 'Mulungu']}, {'Jeriva': []}, {'Capororoca': ['Aroeira', 'Jeriva']}, {'Mulungu': []}, {'Embauba': []}, {'Aroeira': ['Embauba', 'Jeriva', 'Mulungu', 'Pitangueira']}]
__ipynb['confusion_matrix_interpretation'] = "Falso"
##### Performance
__ipynb['performance_tuning'] = "Sim, uma vez, mudando o que? Melhorou?"
__ipynb['performance_tuning_text'] = "Acurácia"
##### New objects
__ipynb['real_objects'] = ['Aroeira', 'Aroeira', 'Aroeira', 'Aroeira', 'Aroeira']
__ipynb['predicted_objects'] = ['Aroeira', 'Aroeira', 'Aroeira', 'Aroeira', 'Aroeira']
__ipynb['predicted_success_times'] = 5
__ipynb['predicted_success_interpretation'] = "Verdadeiro"

jupic = JupIC(__ipynb)
score = evaluate(jupic)
print(score)
write_json(jupic)
display(score['total_score'])