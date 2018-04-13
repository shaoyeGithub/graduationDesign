import os
import numpy as np
from keras.preprocessing.image import  load_img, img_to_array
from keras.models import load_model

img_width, img_height = 150, 150
model_path = './models/model.h5'
model_weights_path = './models/weights.h5'
model = load_model(model_path)
model.load_weights(model_weights_path)

def predict(file):
  x = load_img(file, target_size=(img_width,img_height))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = model.predict(x)
  result = array[0]
  #answer = np.argmax(result)
  if result.max() == 0.0:
    return True
  else:
    return False

# counter = 1
# while counter<=623:
# 	#name ='cat2.jpg'
# 	name = 'data/train/trainN/negative_'+str(counter).zfill(3)+'.jpg'
# 	result = predict(name)
# 	counter = counter +1
