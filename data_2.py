# -*- coding: utf-8 -*-
"""data-2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oGWIfca9QOhV9PSsrnHbwWG6ZSNmDdk8

Süeda Sena SÖNMEZ-180255023-İ.Ö
"""

from keras.models import Sequential
from numpy import loadtxt
from keras.layers import Dense,Dropout
from sklearn.preprocessing import LabelEncoder
from google.colab import drive
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sbn
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import mean_squared_error,r2_score
from sklearn import model_selection
from sklearn.neighbors import KNeighborsRegressor
from warnings import filterwarnings
filterwarnings("ignore")
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

drive.mount('/content/drive')

dataset=pd.read_excel(r'/content/drive/MyDrive/Derinogrenme/data-2.xlsx')
dataset.shape

dataset

dataset.columns

dataset['Class'].unique()

y_data=dataset['Class']
y_data

dataset=pd.get_dummies(dataset,columns=['Class'])
dataset

x = dataset[['Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength',
       'AspectRation', 'Eccentricity', 'ConvexArea', 'EquivDiameter', 'Extent',
       'Solidity', 'roundness', 'Compactness', 'ShapeFactor1', 'ShapeFactor2',
       'ShapeFactor3', 'ShapeFactor4']]

y = dataset[['Class_BARBUNYA', 'Class_BOMBAY', 'Class_CALI',
       'Class_DERMASON', 'Class_HOROZ', 'Class_SEKER', 'Class_SIRA']]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=42,shuffle=True)

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

from keras import regularizers
model = Sequential()
model.add(Dense(256,input_shape=[x.shape[1]], activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dense(128,kernel_regularizer=regularizers.l2(0.01),activation="relu"))
model.add(Dense(y.shape[1], activation='softmax'))
model.summary()

model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])

history=model.fit(x_train,y_train,epochs=200,batch_size=10, validation_split=0.1)

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

scores = model.evaluate(x_train,y_train)
print("Training Accuracy: %.2f%%\n" % (scores[1]*100))
scores = model.evaluate(x_test,y_test)
print("Testing Accuracy: %.2f%%\n" % (scores[1]*100))

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
y_pred_test = model.predict(x_test)
y_pred=[]

for i in y_pred_test:
  if(i>=0.1):
    y_pred.append(1)
  else:
    y_pred.append(0)
print(y_pred)
cm = confusion_matrix(y_test,y_pred)
ax = sns.heatmap(cm, annot=True, xticklabels=['Class_BARBUNYA', 'Class_BOMBAY', 'Class_CALI',
       'Class_DERMASON', 'Class_HOROZ', 'Class_SEKER', 'Class_SIRA'], yticklabels=['Class_BARBUNYA', 'Class_BOMBAY', 'Class_CALI',
       'Class_DERMASON', 'Class_HOROZ', 'Class_SEKER', 'Class_SIRA'],
                cbar=False,cmap='Blues')
ax.set_xlabel('Prediction')
ax.set_ylabel('Actual')
plt.show()