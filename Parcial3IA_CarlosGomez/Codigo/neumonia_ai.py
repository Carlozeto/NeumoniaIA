# -*- coding: utf-8 -*-
"""NEUMONIA_AI

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aTeiRJcZ3cG8qC9yfrTTh36jP7D73BrD
"""

from datetime import datetime
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

from tensorflow.keras.layers import MaxPooling2D, AveragePooling2D, Flatten, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras import regularizers

from keras.models import Model, load_model
from keras.layers import Input, Flatten, Dense
from tensorflow.keras.layers import Dropout, Lambda
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, DepthwiseConv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import concatenate
from keras import optimizers
from keras.layers import BatchNormalization


from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd, numpy as np

from sklearn.model_selection import train_test_split
import glob, cv2, numpy as np
from tqdm import tqdm

from keras.datasets import cifar10
from matplotlib import pyplot
import zipfile
import sys

from google.colab import drive
drive.mount('/content/gdrive')

!ls /content/gdrive/MyDrive/data

!unzip /content/gdrive/MyDrive/data/neumonia2.zip

start = datetime.now()


categorias = ['NORMAL', 'PNEUMONIA']

X = []
Y = []
X2 = []
Y2 = []
for categoria in tqdm(categorias):
  ruta_imgs = glob.glob('./chest_xray/train/'+ categoria +'/*.jpeg')
  for ruta_img in ruta_imgs:
    img = cv2.resize(cv2.cvtColor(cv2.imread(ruta_img), cv2.COLOR_RGB2BGR), (150, 150))

    '''grayScale = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    kernel = cv2.getStructuringElement(1,(17,17))
    blackhat = cv2.morphologyEx(grayScale,cv2.MORPH_BLACKHAT,kernel)
    ret, threshold = cv2.threshold(blackhat, 10,255, cv2.THRESH_BINARY)
    final_image = cv2.inpaint(img,threshold, 1, cv2.INPAINT_TELEA)'''
    img_blurred = cv2.GaussianBlur(img, (5, 5), 0)  # Aplica un filtro Gaussiano 5x5

    X.append(img)
    if categoria == 'NORMAL':
      Y.append(0)
    else:
      Y.append(1)

    X2.append(img_blurred)
    if categoria == 'NORMAL':
      Y2.append(0)
    else:
      Y2.append(1)


X = np.asarray(X).astype('uint8')
Y = np.expand_dims(np.asarray(Y).astype('uint8'), axis = 1)

X2 = np.asarray(X2).astype('uint8')
Y2 = np.expand_dims(np.asarray(Y2).astype('uint8'), axis = 1)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

x2_train, x2_test, y2_train, y2_test = train_test_split(X2, Y2, test_size=0.2, random_state=42)

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

print(x_train.shape, x_test.shape)
print(y_train.shape, y_test.shape)

for i in range(9):
	pyplot.subplot(330 + 1 + i)
	pyplot.imshow(x_train[i])
pyplot.show()

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

x_train /= 255.0
x_test /= 255.0

y2_train = to_categorical(y2_train)
y2_test = to_categorical(y2_test)

x2_train = x2_train.astype('float32')
x2_test = x2_test.astype('float32')

x2_train /= 255.0
x2_test /= 255.0

model = Sequential()
model.add(Input((150, 150, 3)))

model.add(Conv2D(64, 3, padding='same', activation='relu'))
model.add(Conv2D(64, 3, padding='same', activation='relu'))
model.add(Conv2D(64, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
'''model.add(Dropout(0.5))
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())

model.add(Dropout(0.2))'''



model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(128, kernel_regularizer = regularizers.l2(1e-5), activation='relu'))
model.add(Dense(64, kernel_regularizer = regularizers.l2(1e-5), activation='relu'))




'''model.add(Conv2D(512, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(256, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Dropout(0.5))
model.add(Conv2D(128, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(64, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(64, 3, padding='same', activation='relu'))
model.add(MaxPooling2D())
model.add(Dropout(0.2))'''
model.add(Flatten())
model.add(Dense(128, kernel_regularizer = regularizers.l2(1e-5), activation='relu'))
model.add(Dense(64, kernel_regularizer = regularizers.l2(1e-5), activation='relu'))

model.add(Dense(2, activation='softmax'))

model.summary()

learning_rate= 1e-4
model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])
'''loss="sparse_categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=["accuracy"]  loss="categorical_crossentropy"  loss=tf.keras.metrics.CategoricalCrossentropy()'''

print(model.output_shape)
'''y_test = to_categorical(y_test, num_classes=10)
y_test = y_test.reshape(-1, 3)'''
print(y_test.shape)

model.fit(x_train, y_train, batch_size= 128, epochs=30, verbose=1, validation_data=(x_test, y_test))

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(loss, acc)

y_pred = model.predict(x_test, verbose=1)
y_pred = np.argmax(y_pred, axis=1)

target_names = ['NORMAL', 'PNEUMONIA']

cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (2,2))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y_test, axis=1), y_pred, target_names=target_names)
print(reporte)

end = datetime.now()
print( end - start)

model.fit(x2_train, y2_train, batch_size= 128, epochs=30, verbose=1, validation_data=(x2_test, y2_test))

loss, acc = model.evaluate(x2_test, y2_test, verbose=0)
print(loss, acc)

y2_pred = model.predict(x2_test, verbose=1)
y2_pred = np.argmax(y2_pred, axis=1)

cm = confusion_matrix(np.argmax(y2_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (2,2))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y2_test, axis=1), y2_pred, target_names=target_names)
print(reporte)

end = datetime.now()
print( end - start)

"""#Posterior a la ejecucion del algoritmo, se almacena el modelo, para despues realizar la validacion de este proceso."""

model.save("pneumonia.h5")
model.save_weights('pneumonia.h5')

"""#Se inicia un nuevo proceso

#implementando el modelo  de imagenet Xception con
"""

nstar= datetime.now()
from tensorflow.keras.applications import Xception


x_model = Xception(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

x_model.summary()

for layer in x_model.layers[:19]:
    layer.trainable = False


for i, layer in enumerate(x_model.layers):
    print(i, layer.name, layer.trainable)

x = x_model.output
x = Flatten()(x)
x= BatchNormalization()(x)
x = Dense(512, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(2, activation='softmax')(x)
x_model.summary()

x_custom_model = Model(inputs=x_model.input, outputs=x)
x_custom_model.summary()

learning_rate= 1e-4
x_custom_model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=["accuracy"])

"""## SIN FILTRO"""

x_custom_model.fit(x_train, y_train, batch_size=128, epochs=20, verbose=1, validation_data=(x_test, y_test))

loss, acc = x_custom_model.evaluate(x_test, y_test, verbose=0)

print(loss, acc)

y_pred = x_custom_model.predict(x_test, verbose=1)
y_pred = np.argmax(y_pred, axis=1)

target_names = ['NORMAL', 'PNEUMONIA']

cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y_test, axis=1), y_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

x_model.summary()
x_model.save("model_X.h5")
x_model.save_weights('pesos_X.h5')

"""## CON FILTRO"""

x_custom_model.fit(x2_train, y2_train, batch_size=128, epochs=20, verbose=1, validation_data=(x2_test, y2_test))

loss, acc = x_custom_model.evaluate(x2_test, y2_test, verbose=0)

print(loss, acc)

y2_pred = x_custom_model.predict(x2_test, verbose=1)
y2_pred = np.argmax(y2_pred, axis=1)

target_names = ['NORMAL', 'PNEUMONIA']

cm = confusion_matrix(np.argmax(y2_test, axis=1), y2_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y2_test, axis=1), y2_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

"""#Se almacena el segundo entrenamiento de Imagenet Xception"""

x_model.summary()
x_model.save("model_X2.h5")
x_model.save_weights('pesos_X2.h5')

"""#0000000000000000000000000000000000000000000000000000

#implementando el modelo  de imagenet VGG16
"""

nstar= datetime.now()
from tensorflow.keras.applications import VGG19


vgg_model = VGG19(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

vgg_model.summary()

for layer in vgg_model.layers[:19]:
    layer.trainable = False


for i, layer in enumerate(vgg_model.layers):
    print(i, layer.name, layer.trainable)

x = vgg_model.output
x = Flatten()(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dense(2, activation='softmax')(x)
vgg_model.summary()

vgg_custom_model = Model(inputs=vgg_model.input, outputs=x)
vgg_custom_model.summary()

learning_rate= 1e-4
vgg_custom_model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=["accuracy"])

"""## SIN FILTRO"""

vgg_custom_model.fit(x_train, y_train, batch_size=128, epochs=20, verbose=1, validation_data=(x_test, y_test))

loss, acc = vgg_custom_model.evaluate(x_test, y_test, verbose=0)

print(loss, acc)

y_pred = vgg_custom_model.predict(x_test, verbose=1)
y_pred = np.argmax(y_pred, axis=1)

target_names = ['NORMAL', 'PNEUMONIA']

cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y_test, axis=1), y_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

visualkeras.layered_view(vgg_custom_model, to_file='VGG.png', legend=False,).show()

vgg_custom_model.summary()
vgg_custom_model.save("model_VGG.h5")
vgg_custom_model.save_weights('pesos_VGG.h5')

"""88888888888888888888888888

## CON FILTRO
"""

vgg_custom_model.fit(x2_train, y2_train, batch_size=128, epochs=20, verbose=1, validation_data=(x2_test, y2_test))

loss, acc = vgg_custom_model.evaluate(x2_test, y2_test, verbose=0)

print(loss, acc)

y2_pred = vgg_custom_model.predict(x_test, verbose=1)
y2_pred = np.argmax(y2_pred, axis=1)

target_names = ['NORMAL', 'PNEUMONIA']

cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y2_test, axis=1), y2_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

vgg_custom_model.summary()
vgg_custom_model.save("model_VGG2.h5")
vgg_custom_model.save_weights('pesos_VGG2.h5')

"""88888888888888888888888888

#implementando el modelo  de imagenet EfficientNetB7
"""

nstar= datetime.now()
from tensorflow.keras.applications import EfficientNetB7


ef_model = EfficientNetB7(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

ef_model.summary()

for layer in ef_model.layers[:19]:
    layer.trainable = False

for i, layer in enumerate(ef_model.layers):
    print(i, layer.name, layer.trainable)

x = ef_model.output
x = Flatten()(x)
x = BatchNormalization()(x)
x = Dense(512, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(2, activation='softmax')(x)
ef_model.summary()

ef_custom_model = Model(inputs=ef_model.input, outputs=x)
ef_custom_model.summary()

learning_rate= 1e-4
ef_custom_model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=["accuracy"])

"""## SIN FILTRO"""

ef_custom_model.fit(x_train, y_train, batch_size=32, epochs=20, verbose=1, validation_data=(x_test, y_test))

loss, acc = ef_custom_model.evaluate(x_test, y_test, verbose=0)

print(loss, acc)

y_pred = ef_custom_model.predict(x_test, verbose=1)
y_pred = np.argmax(y_pred, axis=1)

cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y_test, axis=1), y_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

visualkeras.layered_view(ef_model, to_file='EfficientNetB7.png', legend=False,).show()

ef_model.summary()
ef_model.save("model_EF.h5")
ef_model.save_weights('pesos_EF.h5')

"""7777777777777777777

## CON FILTRO
"""

ef_custom_model.fit(x2_train, y2_train, batch_size=32, epochs=20, verbose=1, validation_data=(x2_test, y2_test))

loss, acc = ef_custom_model.evaluate(x2_test, y2_test, verbose=0)

print(loss, acc)

y2_pred = ef_custom_model.predict(x2_test, verbose=1)
y2_pred = np.argmax(y2_pred, axis=1)

cm = confusion_matrix(np.argmax(y2_test, axis=1), y2_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y2_test, axis=1), y2_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

ef_model.summary()
ef_model.save("model_EF2.h5")
ef_model.save_weights('pesos_EF2.h5')

"""7777777777777777777

#implementando el modelo  de imagenet ResNet50V2
"""

nstar= datetime.now()
from tensorflow.keras.applications import ResNet50V2


rn_model = ResNet50V2(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

rn_model.summary()

for layer in rn_model.layers[:19]:
    layer.trainable = False

for i, layer in enumerate(rn_model.layers):
    print(i, layer.name, layer.trainable)

x = rn_model.output
x = Flatten()(x)
x = BatchNormalization()(x)
x = Dense(512, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(2, activation='softmax')(x)
rn_model.summary()

rn_custom_model = Model(inputs=rn_model.input, outputs=x)
rn_custom_model.summary()

learning_rate= 1e-4
rn_custom_model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=learning_rate), metrics=["accuracy"])

"""## SIN FILTRO"""

rn_custom_model.fit(x_train, y_train, batch_size=64, epochs=20, verbose=1, validation_data=(x_test, y_test))

loss, acc = rn_custom_model.evaluate(x_test, y_test, verbose=0)

print(loss, acc)

y_pred = rn_custom_model.predict(x_test, verbose=1)
y_pred = np.argmax(y_pred, axis=1)

cm = confusion_matrix(np.argmax(y_test, axis=1), y_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y_test, axis=1), y_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

!pip install pillow==9.5.0
!pip install --upgrade visualkeras
import visualkeras
visualkeras.layered_view(rn_custom_model, to_file='ResNet50V2.png', legend=False).show()

rn_custom_model.summary()
rn_custom_model.save("model_RN.h5")
rn_custom_model.save_weights('pesos_RN.h5')

"""## CON FILTRO"""

rn_custom_model.fit(x2_train, y2_train, batch_size=64, epochs=20, verbose=1, validation_data=(x2_test, y2_test))

loss, acc = rn_custom_model.evaluate(x2_test, y2_test, verbose=0)

print(loss, acc)

y2_pred = rn_custom_model.predict(x2_test, verbose=1)
y2_pred = np.argmax(y2_pred, axis=1)

cm = confusion_matrix(np.argmax(y2_test, axis=1), y2_pred)
cm = pd.DataFrame(cm,  range(2),range(2))
plt.figure(figsize = (10,10))

sns.heatmap(cm, annot=True, annot_kws={"size": 14},fmt="d",linewidths=.5,xticklabels=target_names, yticklabels=target_names,cmap="YlGnBu" ) # font size
plt.show()

reporte = classification_report(np.argmax(y2_test, axis=1), y2_pred, target_names=target_names)
print(reporte)

nend = datetime.now()
print( nend - nstar)

rn_custom_model.summary()
rn_custom_model.save("model_RN2.h5")
rn_custom_model.save_weights('pesos_RN2.h5')