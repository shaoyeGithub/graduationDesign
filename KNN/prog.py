import keras       # machine learning built on top of tensor flow
import numpy as np # to do the maths
import os
from PIL import Image as pil_image
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras import optimizers

img_width, img_height = 150, 150

train_data_dir = 'data/train'
validation_data_dir = 'data/validation'

datagen = ImageDataGenerator(rescale=1./255)

# automagically retrieve images and their classes for train and validation sets
train_generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=16,
        class_mode='binary')

validation_generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=32,
        class_mode='binary')

#step 2  - BUILD THE MODEL
model = Sequential()
model.add(Conv2D(32,(3,3),input_shape = (img_width,img_height,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Conv2D(32,(3,3),input_shape = (img_width,img_height,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Conv2D(32,(3,3),input_shape = (img_width,img_height,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss = 'binary_crossentropy',
              optimizer  = 'rmsprop',
              metrics = ['accuracy'])
#step 3- TRAINING THE MODEL
model.fit_generator(
    train_generator,
    steps_per_epoch =100,
    epochs=10,
    validation_data=validation_generator,
    nb_val_samples = 80)
model.save_weights('models/weights.h5')
model.save('models/model.h5')
