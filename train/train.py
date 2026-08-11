"""
Implementation of siamese network 
using keras io as guide 

Goals :

1. Light weight but efficeint model -> Separable conv2d 
2. Efficient Model 

"""

import tensorflow as tf 
import keras 
from keras import layers , Model 
from utils import load_datasets , make_pairs , pairing 

path = r'C:\Users\blade_mx4\Documents\Datasets\DOG_CAT'

X , Y = load_datasets(path)

#print(X.shape) 

#X_train , Y_train = make_pairs(X,Y) 

train_ds = make_pairs(X,Y) 

# ======================================= MODEL ================================== #

def 