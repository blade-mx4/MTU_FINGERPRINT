# functions for the model training 
import tensorflow as tf 
import keras 
from keras import layers , Model 
import numpy as np 
import random
from keras.utils import image_dataset_from_directory 


# ====================== HYPER PARAMETERS ========================== #
SHAPE = (224,224) 


# ===================== UTILS FUNCTIONS ============================ # 

def load_datasets(path) : 
    ds = image_dataset_from_directory(
        path , image_size = SHAPE ,batch_size = None,
        shuffle =True , label_mode = 'int' 
        )

    img , label = [] , [] 

    for imgs ,labels in ds : 
        img.append(imgs.numpy())
        label.append(labels.numpy()) 

    X = np.array(img)
    Y = np.array(label) 

    return X ,Y 


def make_pairs(x, y):   #<-- Didnt write this honestly  from keras io

    """Creates a tuple containing image pairs with corresponding label.

    Arguments:
        x: List containing images, each index in this list corresponds to one image.
        y: List containing labels, each label with datatype of `int`.

    Returns:
        Tuple containing two numpy arrays as (pairs_of_samples, labels),
        where pairs_of_samples' shape is (2len(x), 2,n_features_dims) and
        labels are a binary array of shape (2len(x)).
    """

    num_classes = max(y) + 1
    digit_indices = [np.where(y == i)[0] for i in range(num_classes)]

    pairs = []
    labels = []

    for idx1 in range(len(x)):
        # add a matching example
        x1 = x[idx1]
        label1 = y[idx1]
        idx2 = random.choice(digit_indices[label1])
        x2 = x[idx2]

        pairs += [[x1, x2]]
        labels += [0]

        # add a non-matching example
        label2 = random.randint(0, num_classes - 1)
        while label2 == label1:
            label2 = random.randint(0, num_classes - 1)

        idx2 = random.choice(digit_indices[label2])
        x2 = x[idx2]

        pairs += [[x1, x2]]
        labels += [1]

    return np.array(pairs), np.array(labels).astype("float32")

def pairing (pairs ,labels ,batch_size =32) : 
    x1 = pairs[: , 0 ]
    x2 = pairs[: , 1 ]

    ds = tf.data.Dataset.from_tensor_slices(((x1,x2),labels))  
    ds = ds.shuffle(buffer_size=len(labels)) 
    ds = ds.batch(batch_size) 
    ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE) 

    return ds  
