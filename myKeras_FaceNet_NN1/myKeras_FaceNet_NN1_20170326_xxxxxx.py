# Make sure to run the code from same directory itself,
# like :       python myKerasSmallNN_autoencoder_2layers_xxxxxx_xxxxxx.py
# instead of : python /projects/myKerasNN/myKerasSmallNN_autoencoder_2layers.py
print "myKeras_FaceNet_NN1.py"

'''

# Paths
basePath = os.getcwd()
modelsPath = basePath + '/../MODELS'

# import stuff
sys.path.append(modelsPath)
from importStuffLoadData import *

# for plotting
import matplotlib.pyplot as plt
from pylab import text

nbClasses = 1
date = '2016_11_03'

# for entropies
nbBins = 12

[origImRows, origImCols, origImChannels, (trainImages, trainResults), (valImages, valResults), (testImages, testResults), fullTestImages] = loadData(nbClasses, date)

os.chdir(basePath)


newTrainImages = resizeImages(trainImages, imRows, imCols)
newValImages = resizeImages(valImages, imRows, imCols)
newTestImages = resizeImages(testImages, imRows, imCols)

'''


import numpy as np

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

import os
import sys
import time

# keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Flatten, Lambda, MaxoutDense
from keras.layers.convolutional import Conv1D, Conv2D
from keras.layers.normalization import LRN2D
from keras.layers.pooling import MaxPooling2D
from keras import backend as K
from sklearn.metrics import mean_squared_error

# Save time
timeStr = time.strftime('%Y%m%d_%H%M%S')

# TODO: KL transform
# TODO: Covariance Equalization

# imresize
imRows = 220
imCols = 220
imChannels = 3

# create model

batchSize = 1800
nbEpochs = 100

nn1 = Sequential() #220x220x3

# conv1
nn1.add(Conv2D(64, kernel_size=(7, 7), strides=(2, 2), padding='same', activation='relu', input_shape=(imRows, imCols, imChannels)))

# pool1
nn1.add(MaxPooling2D(pool_size=(3, 3), strides=(2,2), padding='same'))

# rnorm1
nn1.add(LRN2D())

# conv2a
nn1.add(Conv2D(64, kernel_size=(1, 1), strides=(1, 1), padding='same', activation='relu'))

# conv2
nn1.add(Conv2D(192, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'))

# rnorm2
nn1.add(LRN2D())

# pool2
nn1.add(MaxPooling2D(pool_size=(3, 3), strides=(2,2), padding='same'))

# conv3a
nn1.add(Conv2D(192, kernel_size=(1, 1), strides=(1, 1), padding='same', activation='relu'))

# conv3
nn1.add(Conv2D(384, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'))

# pool3
nn1.add(MaxPooling2D(pool_size=(3, 3), strides=(2,2), padding='same'))

# conv4a
nn1.add(Conv2D(384, kernel_size=(1, 1), strides=(1, 1), padding='same', activation='relu'))

# conv4
nn1.add(Conv2D(256, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'))

# conv5a
nn1.add(Conv2D(256, kernel_size=(1, 1), strides=(1, 1), padding='same', activation='relu'))

# conv5
nn1.add(Conv2D(256, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'))

# conv6a
nn1.add(Conv2D(256, kernel_size=(1, 1), strides=(1, 1), padding='same', activation='relu'))

# conv6
nn1.add(Conv2D(256, kernel_size=(3, 3), strides=(1, 1), padding='same', activation='relu'))

# pool4
nn1.add(MaxPooling2D(pool_size=(3, 3), strides=(2,2), padding='same'))

# concat
nn1.add(Flatten())

# fc1
nn1.add(MaxoutDense(4096, nb_feature=2))

# fc2
nn1.add(MaxoutDense(4096, nb_feature=2))

# fc7128
nn1.add(Dense(128))

# L2
nn1.add(Lambda(lambda x: K.l2_normalize(x, axis=1)))


# Compile the model
nn1.compile(optimizer='adam', loss='binary_crossentropy')

# Fit the model
nn1.fit(newTrainImages, newTrainImages,
                batch_size=batchSize,
                nb_epoch=nbEpochs,
                shuffle=True,
                validation_data=(newValImages, newValImages),
                verbose=1)


# Save the model
# Save time
timeStr = time.strftime('%Y%m%d_%H%M%S')
modelName = 'myKerasSmallNNModel_autoencoder_2layers_' + timeStr + '.h5'
nn1.save(modelName)
print "model saved."

'''
# Load the model
modelName = modelsPath + '/myKerasSmallNNModel_autoencoder_2layers_20161112_184710.h5'
autoencoder = load_model(modelName)
'''

# FINDING RANGE OF ENTROPIES

# calc entropy for train
trainPreds = nn1.predict(newTrainImages)
trainEntropies = calcCrossEntropy(newTrainImages, trainPreds, nbBins)

'''
for i in range(trainPreds.shape[0]):
	plotImage = np.concatenate((newTrainImages[i].reshape(imRows, imCols), trainPreds[i].reshape(imRows, imCols)), axis=1)
	plt.imshow(plotImage, cmap='gray')
	plt.show()
'''

'''
# predict, calc entropy for val
valPreds = nn1.predict(newValImages)
valEntropies = calcCrossEntropy(newValImages, valPreds, nbBins)

# predict, calc entropy for test
testPreds = nn1.predict(newTestImages)
testEntropies = calcCrossEntropy(newTestImages, testPreds, nbBins)


# Entropies

print "trainEntropies : " + trainEntropies.min().astype(str) + " ---- " + trainEntropies.max().astype(str)
print "valEntropies   : " + valEntropies.min().astype(str) + " ---- " + valEntropies.max().astype(str)
print "testEntropies  : " + testEntropies.min().astype(str) + " ---- " + testEntropies.max().astype(str)

minEntropy = np.array([trainEntropies.min(), valEntropies.min(), testEntropies.min()]).min()
maxEntropy = np.array([trainEntropies.max(), valEntropies.max(), testEntropies.max()]).max()

minEntropy = -2.62555459586
maxEntropy = -1.87461698778

# TESTING

[origImRows, origImCols, origImChannels, (trainImages, trainResults), (valImages, valResults), (testImages, testResults), fullTestImages] = loadData(2, date)
newTrainImages = resizeImages(trainImages, imRows, imCols)
newValImages = resizeImages(valImages, imRows, imCols)
newTestImages = resizeImages(testImages, imRows, imCols)

# train
trainPreds = nn1.predict(newTrainImages)
trainEntropies = calcCrossEntropy(newTrainImages, trainPreds, nbBins)

trainClass = ((trainEntropies>=minEntropy) & (trainEntropies<=maxEntropy)).astype(int)

trainClassAccuracy = ((trainClass==trainResults).astype(int).sum())/float(trainClass.shape[0])

# full test

newFullTestImages = resizeImages(fullTestImages, imRows, imCols)
fullTestPreds = nn1.predict(newFullTestImages, imRows, imCols)

fullTestEntropies = calcCrossEntropy(newFullTestImages, fullTestPreds)
fulltestClass = ((fullTestEntropies>=minEntropy) & (fullTestEntropies<=maxEntropy)).astype(int)

fullTestClassAccuracy = ((fulltestClass==trainResults).astype(int).sum())/float(trainClass.shape[0])

print

for i in range(fullTestEntropies.shape[0]):
    #plotImage = fullTestImages[i].reshape(origImRows, origImCols)
    plotImage = np.concatenate((newFullTestImages[i].reshape(imRows, imCols), fullTestPreds[i].reshape(imRows, imCols)), axis=1)
    plt.imshow(plotImage, cmap='gray')
    rangeText = "Entropy range : " + str(minEntropy) + " ---- " + str(maxEntropy)
    text(2, 2, rangeText, color='black', fontsize=20)
    text(2.5, 2.5, rangeText, color='white', fontsize=20)
    iEntropyText = fullTestEntropies[i].astype(str)
    text(2, 10, iEntropyText, color='black', fontsize=20)
    text(2.5, 10.5, iEntropyText, color='white', fontsize=20)
    if (fullTestEntropies[i]>=minEntropy)&(fullTestEntropies[i]<=maxEntropy) :
        state='EMPTY_CASKET'
    else:
        state='NOT Empty_casket'
    text(2, 18, state, color='black', fontsize=20)
    text(2.5, 18.5, state, color='white', fontsize=20)
    plt.show()

'''

'''
from keras.datasets import mnist
(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))

input_img = Input(shape=(28, 28, 1))

x = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(input_img)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(x)
encoded = MaxPooling2D((2, 2), border_mode='same')(x)

# at this point the representation is (32, 7, 7)

x = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(encoded)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(32, 3, 3, activation='relu', border_mode='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Convolution2D(1, 3, 3, activation='sigmoid', border_mode='same')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

autoencoder.fit(x_train, x_train,
                nb_epoch=100,
                batch_size=128,
                shuffle=True,
                validation_data=(x_test, x_test))


'''