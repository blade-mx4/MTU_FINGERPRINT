# utils.py
import tensorflow as tf
import numpy as np
import random
import pathlib
import keras
from keras import ops


SHAPE = (224, 224)

def load(path) :
    ds = keras.utils.image_dataset_from_directory (
            path ,
            image_size = (224,224) ,
            batch_size = 8 ,
            label_mode= 'int'
    )
    X ,Y = ds
    return X ,Y 

def make_pairs (x,y) : 
    
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


def euclidean_distance(vector):
    X, Y = vector
    sum_sqr = ops.sum(ops.square(X - Y), axis=1, keepdims=True)
    distance = ops.sqrt(ops.maximum(sum_sqr, keras.backend.epsilon()))
    return distance


def Loss(y_true, y_pred, margin=1):
    """
    Contrastive loss.
    y_true = 0 -> similar pair   -> minimize distance
    y_true = 1 -> dissimilar pair -> push distance >= margin
    """
    squr_pred = ops.square(y_pred)
    margin_sqr = ops.square(ops.maximum(margin - y_pred, 0))
    LOSS = ops.mean((1 - y_true) * squr_pred + y_true * margin_sqr)
    return LOSS

def accuracy(y_true, y_pred):
    """Computes the accuracy of the predictions.

    Arguments:
        y_true: List of labels, each label is of type float32.
        y_pred: List of predictions of same length as of y_true,
                each label is of type float32.

    Returns:
        A tensor containing accuracy as floating point value.
    """
    y_true = ops.cast(y_true, "float32")

    y_true = ops.reshape(y_true, [-1])
    y_pred = ops.reshape(y_pred, [-1])

    # 0 for similar (<0.5), 1 for dissimilar (>0.5)
    preds = ops.cast(y_pred > 0.5, "float32")
    return ops.mean(ops.equal(y_true, preds))
