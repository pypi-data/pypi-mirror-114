class JupIC:  
    '''JupIC is Jupyter image classification task data'''
    # Model
    model_categories = []
    model_correctly_labeled_images = 0
    # Dataset
    dataset_categories_images = []
    dataset_total_images = 0
    # Transfer Learning
    tl_models = []
    tl_epochs = []
    tl_learning_rates = []
    tl_trained = False
    ft_unfreezed = False
    # Fine Tuning
    ft_epochs = []
    ft_learning_rate_found = False
    ft_trained = False
    # Accuracy
    accuracy_categories = []
    accuracy_analysis = False
    accuracy_analysis_categories = []
    accuracy_interpretation = ''
    # Confusion matrix
    confusion_matrix_mislabeled_real = []
    confusion_matrix_mislabeled = []
    confusion_matrix_interpretation = False
    # Performance
    performance_tuning = ''
    performance_tuning_text = ''
    # New objects
    real_objecs = []
    predicted_objects = []
    predicted_success_times = 0
    predicted_success_interpretation = False


    def __init__(
        self,
        __ipynb: dict,
    ): 
        # Model
        self.model_categories = __ipynb['model_categories']
        self.model_correctly_labeled_images = __ipynb['model_correctly_labeled_images']

        # Dataset
        self.dataset_categories_images = __ipynb['dataset_categories_images']
        self.dataset_total_images = __ipynb['dataset_total_images']

        # Transfer Learning
        self.tl_models = __ipynb['tl_models']
        self.tl_epochs = __ipynb['tl_epochs']
        self.tl_learning_rates = __ipynb['tl_learning_rates']
        self.tl_trained = __ipynb['tl_trained']

        # Fine Tuning
        self.ft_unfreezed = __ipynb['ft_unfreezed']
        self.ft_learning_rate_found =  __ipynb['ft_learning_rate_found']
        self.ft_trained = __ipynb['ft_trained']

        # Accuracy
        self.accuracy_categories = __ipynb['accuracy_categories']
        self.accuracy_analysis = string_to_bool(__ipynb['accuracy_analysis'])
        self.accuracy_analysis_categories = __ipynb['accuracy_analysis_categories']
        self.accuracy_interpretation = __ipynb['accuracy_interpretation']   

        # Confusion matrix
        self.confusion_matrix_mislabeled_real = __ipynb['confusion_matrix_mislabeled_real']
        self.confusion_matrix_mislabeled = __ipynb['confusion_matrix_mislabeled']
        self.confusion_matrix_interpretation = string_to_bool(
            __ipynb['confusion_matrix_interpretation'])

        # Performance
        self.performance_tuning = __ipynb['performance_tuning']
        self.performance_tuning_text = __ipynb['performance_tuning_text']
        
        # New objects
        self.real_objects = __ipynb['real_objects']
        self.predicted_objects = __ipynb['predicted_objects']
        self.predicted_success_times = __ipynb['predicted_success_times']
        self.predicted_success_interpretation = string_to_bool(
            __ipynb['predicted_success_interpretation'])


def string_to_bool(text: str) -> bool:
    '''Converts string to bool'''

    if text == 'Verdadeiro': return True 
    return False