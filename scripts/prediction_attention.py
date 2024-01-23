# -*- coding:utf-8 -*-
# modified from https://github.com/mayuefine/c_AMPs-prediction/tree/master

## usage python prediction_attention.py bact.txt att_bact.txt
import tensorflow as tf

from keras.models import load_model
from numpy import loadtxt, savetxt
from Attention import Attention_layer
from sys import argv

# Setting the device to GPU if available
device_name = tf.test.gpu_device_name()
if device_name:
    print('Found GPU at: {}'.format(device_name))
else:
    print("GPU device not found, using CPU instead.")

model = load_model('Models/att.h5', custom_objects={'Attention_layer': Attention_layer})
x = loadtxt(argv[1], delimiter=",", encoding='utf-8')

# Use the GPU for prediction
with tf.device('/GPU:0'):
    preds = model.predict(x)

savetxt(argv[2], preds, fmt="%.8f", delimiter=",")

