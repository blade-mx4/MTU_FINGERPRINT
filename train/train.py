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
from utils import load,euclidean_distance, Loss,accuracy
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.model_selection import train_test_split 
import numpy as np 

# =========================================DATA LOADING AND HYPER PARAM============================================ #

path = r'C:\Users\blade_mx4\Documents\Datasets\DOG_CAT'

X , Y = load(path) 

x_train , __ , y_train ,__ = train_test_split(X, Y ,random_state=42,test_size=0.2)

X = np.array(X)
print(X.shape)

"""
# ======================================= EMBEDDING MODEL ================================== #

def build_embedding_model():
    Input = layers.Input((224, 224, 3))
    x = layers.Rescaling(scale=1./127.5, offset=-1)(Input)

    x = layers.Conv2D(16, kernel_size=(3, 3), strides=(1, 1), activation='tanh')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(32, kernel_size=(3, 3), strides=(1, 1), activation='tanh')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.BatchNormalization()(x)

    x = layers.SeparableConv2D(64, kernel_size=(3, 3), strides=(1, 1), activation='tanh')(x)
    x = layers.SeparableConv2D(128, kernel_size=(3, 3), strides=(1, 1), activation='tanh')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.BatchNormalization()(x)

    x = layers.AveragePooling2D(pool_size=(2, 2))(x)
    x = layers.Dropout(0.2)(x)          # <-- fixed: now reassigned
    x = layers.Flatten()(x)

    x = layers.BatchNormalization()(x)

    x = layers.Dense(64, activation='tanh')(x)   # embedding, pre-normalization
    x = layers.UnitNormalization()(x)            # <-- L2-normalize so distances live in [0, 2]

    return keras.Model(Input, x)


EMBED = build_embedding_model()     
EMBED.summary()

# ======================================== SIAMESE MODEL HEAD ============================================ #

Input_A = layers.Input((224, 224, 3))
Input_B = layers.Input((224, 224, 3))

Vector_A = EMBED(Input_A)
Vector_B = EMBED(Input_B)

distance = layers.Lambda(euclidean_distance)([Vector_A, Vector_B])
Siamese = keras.Model(inputs=[Input_A, Input_B], outputs=distance)

Siamese.summary()

# ============================================ TRAINING =================================================== #

Siamese.compile(
    loss=Loss,
    optimizer=keras.optimizers.RMSprop(learning_rate=0.001),  
    jit_compile=True,metrics=[accuracy]
)

reduce = ReduceLROnPlateau(
    patience=10, cooldown=2,
    verbose=1, factor=0.2,
    mode='auto'
)

earlystop = EarlyStopping(
    patience=20, mode='auto',
    verbose=1, start_from_epoch=5,
    restore_best_weights=True
)

auto_save = ModelCheckpoint(
    'save_model.keras',
    save_best_only=True
)

Siamese.fit(
    train, epochs=35, callbacks=[reduce, earlystop, auto_save] 
)
Siamese.save("MODEL.keras")"""