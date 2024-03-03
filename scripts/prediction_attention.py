import pandas as pd
from keras.models import load_model
import tensorflow as tf
from Attention import Attention_layer
from sys import argv

# Load the model
model = load_model('Models/att.h5', custom_objects={'Attention_layer': Attention_layer})

# Use pandas to read the CSV file. Adjust the dtype if you know the exact data types to save memory.
x = pd.read_csv(argv[1], delimiter=",", encoding='utf-8', dtype='float32')

# Predictions
with tf.device('/GPU:0'):
    preds = model.predict(x.values)

# Save predictions to CSV. Adjust path as necessary.
preds_df = pd.DataFrame(preds)
preds_df.to_csv(argv[2].replace('\xa0', ''), index=False, float_format="%.8f")


