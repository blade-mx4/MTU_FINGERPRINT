# functions for the model training 
import tensorflow as tf 

import keras 
from keras import layers , Model 
from keras.utils import image_dataset_from_directory ,load_img , img_to_array
import numpy as np 
import random



SHAPE = (224,224)

def load_imgs(path) : 
    ds = image_dataset_from_directory (
        path , image_size=(224,224) , batch_size = 16 ,
        label_mode='int' 
    )
    return ds 
