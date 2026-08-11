# utils.py
import tensorflow as tf
import numpy as np
import random
import pathlib
import keras
from keras import ops


SHAPE = (224, 224)


def get_filepaths_and_labels(path):
    """Collects file paths and integer labels WITHOUT loading images into memory."""
    path = pathlib.Path(path)
    class_names = sorted([d.name for d in path.iterdir() if d.is_dir()])
    class_to_idx = {name: idx for idx, name in enumerate(class_names)}

    filepaths = []
    labels = []
    for class_name in class_names:
        for f in (path / class_name).glob("*"):
            filepaths.append(str(f))
            labels.append(class_to_idx[class_name])

    return np.array(filepaths), np.array(labels), class_names


def make_pair_indices(y):
    """Builds pairs of INDICES (not images) — cheap, just integers.

    Label convention (matches standard contrastive loss):
        0 -> similar pair (same class)
        1 -> dissimilar pair (different class)
    """
    num_classes = max(y) + 1
    class_indices = [np.where(y == i)[0] for i in range(num_classes)]

    pairs = []
    labels = []

    for idx1 in range(len(y)):
        label1 = y[idx1]
        idx2 = random.choice(class_indices[label1])
        pairs.append([idx1, idx2])
        labels.append(0)  # same class -> similar

        label2 = random.randint(0, num_classes - 1)
        while label2 == label1:
            label2 = random.randint(0, num_classes - 1)
        idx2 = random.choice(class_indices[label2])
        pairs.append([idx1, idx2])
        labels.append(1)  # different class -> dissimilar

    return np.array(pairs), np.array(labels).astype("float32")


def load_and_preprocess(filepath):
    img = tf.io.read_file(filepath)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.resize(img, SHAPE)
    return img


def build_pair_dataset(filepaths, pair_indices, pair_labels, batch_size=16):
    """Lazily loads only the images needed for each batch, on the fly."""
    idx1 = pair_indices[:, 0]
    idx2 = pair_indices[:, 1]

    ds = tf.data.Dataset.from_tensor_slices(((idx1, idx2), pair_labels))
    ds = ds.shuffle(buffer_size=len(pair_labels))

    def load_pair(idx_pair, label):
        i1, i2 = idx_pair
        path1 = tf.gather(filepaths, i1)
        path2 = tf.gather(filepaths, i2)
        img1 = load_and_preprocess(path1)
        img2 = load_and_preprocess(path2)
        return (img1, img2), label

    ds = ds.map(load_pair, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(tf.data.AUTOTUNE)

    return ds


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