# -*- coding: utf-8 -*-
"""SC_Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16LH6r93ACKUEY7iMYK4gc41HVNkaGAAz

# Importing
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import tensorflow as tf
from tensorflow import keras
import seaborn as sn
from sklearn.model_selection import train_test_split

"""# Mounting"""

from google.colab import drive
drive.mount('/content/drive')

"""# Read Dataset"""

url = '/content/drive/My Drive/Colab Notebooks/datasets/firmware.csv'

df = pd.read_csv(url)
df.head()

"""# Pre-processing

"""

df = df.drop(columns=['filename', 'class'])
df.head()

df = df.dropna(axis='columns')
df.head()

df_label = df['target']
df = df.drop(columns=['target'])
df.head()

data = df.to_numpy()
data = np.reshape(data, (-1, 32,32))
data

data.shape

labels = df_label.to_numpy()

"""# Splitting Dataset"""

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=30)

x_train.shape

y_train.shape

"""# Testing NN"""

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(32, 32)),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(3, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test, y_test)

y_predict = model.predict(x_test)
y_predict[0]

np.argmax(y_predict[0])

y_predict_labels = [np.argmax(i) for i in y_predict]
y_predict_labels[:5]

cm = tf.math.confusion_matrix(labels=y_test, predictions=y_predict_labels)
cm

plt.figure(figsize=(10,7))
sn.heatmap(cm, annot=True, fmt='d', cmap="coolwarm")
plt.xlabel('Predicted')
plt.ylabel('True')

from sklearn import metrics
print(metrics.classification_report(y_test, y_predict_labels))

"""# ANN"""

ann = keras.Sequential([
    keras.layers.Flatten(input_shape=(32, 32)),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(3, activation='sigmoid')
])

adam = keras.optimizers.Adam(learning_rate=0.001)
ann.compile(
    optimizer=adam,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

ann_history = ann.fit(x_train, y_train, epochs=5, batch_size=20)

ann_history.history

plt.plot(ann_history.history['loss'])
plt.title('ANN')
plt.ylabel('Sparse Categorical Crossentropy Value')
plt.xlabel('No. Epoch')
plt.show()

ann.evaluate(x_test, y_test)

y_predict = ann.predict(x_test)
y_predict_labels = [np.argmax(i) for i in y_predict]

from sklearn import metrics
print ('Accuracy: ', metrics.accuracy_score(y_test, y_predict_labels))
print ('Precision: ', metrics.precision_score(y_test, y_predict_labels, average='micro'))
print ('Recall: ', metrics.recall_score(y_test, y_predict_labels, average='micro'))
print ('F1-score: ', metrics.f1_score(y_test, y_predict_labels, average='micro'))

"""# CNN


"""

cnn = keras.Sequential([
    # cnn
    keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 1)),
    keras.layers.MaxPooling2D((2, 2)),

    # dense
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(3, activation='sigmoid')
])

adam = keras.optimizers.Adam(learning_rate=0.001)
cnn.compile(
    optimizer=adam,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

cnn_history = cnn.fit(x_train, y_train, epochs=5, batch_size=20)

plt.plot(cnn_history.history['loss'])
plt.title('Loss VS Epoch')
plt.ylabel('Sparse Categorical Crossentropy Value')
plt.xlabel('No. Epoch')
plt.show()

cnn.evaluate(x_test, y_test)

y_predict = cnn.predict(x_test)
y_predict_labels = [np.argmax(i) for i in y_predict]

from sklearn import metrics
print ('Accuracy: ', metrics.accuracy_score(y_test, y_predict_labels))
print ('Precision: ', metrics.precision_score(y_test, y_predict_labels, average='micro'))
print ('Recall: ', metrics.recall_score(y_test, y_predict_labels, average='micro'))
print ('F1-score: ', metrics.f1_score(y_test, y_predict_labels, average='micro'))

"""# Loss VS Epoch"""

plt.plot(cnn_history.history['loss'], label='CNN Loss')
plt.plot(ann_history.history['loss'], label='ANN Loss')
plt.title('Loss VS Epoch')
plt.ylabel('Sparse Categorical Crossentropy Value')
plt.xlabel('No. Epoch')
plt.legend(loc="upper left")
plt.show()