"""
Implementation of siamese network 
using keras io as guide 

Goals :
1. Light weight but efficient model -> Separable conv2d 
2. Efficient Model 
"""

import tensorflow as tf 
import keras 
from keras import layers 
from utils import get_filepaths_and_labels, make_pair_indices, build_pair_dataset,euclidean_distance


# =========================================DATA LOADING AND HYPER PARAM============================================ #

path = r'C:\Users\blade_mx4\Documents\Datasets\DOG_CAT'


filepaths, labels, class_names = get_filepaths_and_labels(path)
pair_indices, pair_labels = make_pair_indices(labels)

filepaths_tensor = tf.constant(filepaths)  # needed for tf.gather inside the tf.data graph
train = build_pair_dataset(filepaths_tensor, pair_indices, pair_labels, batch_size=8)

# ======================================= MODEL ================================== #

Input_A = layers.Input((224,224,3))
Input_B = layers.Input((224,224,3))


def Model() : 
    Input = layers.Input((224,224,3))  
    x = layers.Rescaling(scale=1./127.5, offset=-1)(Input)

    x = layers.Conv2D(16, kernel_size=(3,3), strides=(1,1), activation='tanh')(x) 
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(32, kernel_size=(3,3), strides=(1,1), activation='tanh')(x) 
    x = layers.MaxPooling2D()(x)
    x = layers.BatchNormalization()(x)

    x = layers.SeparableConv2D(64, kernel_size=(3,3), strides=(1,1), activation='tanh')(x) 
    x = layers.SeparableConv2D(128, kernel_size=(3,3), strides=(1,1), activation='tanh')(x) 
    x = layers.MaxPooling2D()(x)
    x = layers.BatchNormalization()(x)


    x = layers.AveragePooling2D(pool_size=(2,2))(x)
    layers.Dropout(0.2)(x)
    x = layers.Flatten()(x)

    x = layers.BatchNormalization()(x) 

    x = layers.Dense(64, activation='tanh')(x)  # final embedding layer, 64D
    return keras.Model(Input, x) 

Model().summary() 
EMBED = Model()
# ======================================== SIAMESE MODEL HEAD ============================================ # 

Vector_A = EMBED(Input_A)
Vector_B = EMBED(Input_B) 

distance = layers.Lambda(euclidean_distance)([Vector_A , Vector_B]) #<-- FIniding distance between this 2 vectors 
Siamese = keras.Model(inputs=[Input_A , Input_B],outputs =distance ) 

Siamese.summary()