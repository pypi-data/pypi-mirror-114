from IPython.display import Image
import os

def display(
    score: int,
):
    '''Displays ninja robot image on Jupyter Notebook'''

    current_path, _ = os.path.split(__file__) 
    image_path = "assets/{0}.png".format(score)
    path = os.path.join(current_path, image_path)

    Image(path)   