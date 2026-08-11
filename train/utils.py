# functions for the model training 
import tensorflow as tf 
import keras 
from keras import layers , Model 
import numpy as np 
import random
from keras.utils import image_dataset_from_directory 
SHAPE = (224,224) 

def load_datasets(path) : 
    image_dataset_from_directory(
        path , image_size = (244,244) ,
        shuffle =True , label_mode = 'int' 
    )
    