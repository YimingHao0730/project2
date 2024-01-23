# -*- coding:utf-8 -*-
# modified from https://github.com/mayuefine/c_AMPs-prediction/tree/master
## usage python prediction_lstm.py sequence_after_format.txt lstm_bact.txt
import tensorflow as tf

# Check if TensorFlow has access to GPU
if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("GPU device not found, using CPU instead.")

from keras.models import load_model
from numpy import loadtxt, savetxt
from sys import argv

model = load_model('Models/lstm.h5')
x = loadtxt(argv[1], delimiter=",")

preds = model.predict(x)
savetxt(argv[2], preds, fmt="%.8f", delimiter=",")
