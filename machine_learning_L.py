#%%
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output
from six.moves import urllib

import tensorflow.compat.v2.feature_column as fc
import tensorflow as tf

# Load the Titanic dataset from Google Cloud Storage
dftrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv')
dfeval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')

# Separate the target variable 'survived' from the features for training and evaluation
y_train = dftrain.pop('survived')
y_eval = dfeval.pop('survived')

# List of categorical and numeric feature columns
CATEGORICAL_COLUMNS = ['sex', 'n_siblings_spouses', 'parch', 'class', 'deck', 'embark_town', 'alone']
NUMERIC_COLUMNS = ['age', 'fare']

# Create a list to hold TensorFlow feature columns
feature_columns = []

# Create categorical feature columns based on unique values in each categorical column
for feature_name in CATEGORICAL_COLUMNS:
    vocabulary = dftrain[feature_name].unique()
    feature_columns.append(tf.feature_column.categorical_column_with_vocabulary_list(feature_name, vocabulary))

# Create numeric feature columns for numeric columns
for feature_name in NUMERIC_COLUMNS:
    feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

#%%
def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
    """Create an input function for the model.

    Args:
        data_df: DataFrame containing the feature data.
        label_df: Series containing the target labels.
        num_epochs: Number of times to go through the dataset.
        shuffle: Boolean to shuffle the dataset or not.
        batch_size: Number of samples in each batch.
        
    Returns:
        A function that creates a tf.data.Dataset object.
    """
    def input_function():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
            ds = ds.shuffle(1000)  # Shuffle the dataset if specified
        ds = ds.batch(batch_size).repeat(num_epochs)  # Create batches and repeat
        return ds
    return input_function

# Create input functions for training and evaluation
train_input_fn = make_input_fn(dftrain, y_train)
eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)

#%%
# Create a dataset to visualize the feature and label batches
ds = make_input_fn(dftrain, y_train, batch_size=13)()
#for feature_batch, label_batch in ds.take(1):
#    print('Some feature keys:', list(feature_batch.keys()))
#    print()
#    print('A batch of class:', feature_batch['class'].numpy())
#    print()
#    print('A batch of Labels:', label_batch.numpy())

#%%
# Create a Linear Classifier model using the feature columns
linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns)

# Train the model using the training input function
linear_est.train(train_input_fn)

# Evaluate the model using the evaluation input function
#result = linear_est.evaluate(eval_input_fn)

# Clear the output for a clean display
#clear_output()

# Print the accuracy of the model
#print(result['accuracy'])

# Make predictions using the evaluation input function
result = list(linear_est.predict(eval_input_fn))

# Print the probability of survival for the first example in the evaluation set
print(result[0]['probabilities'][0])
