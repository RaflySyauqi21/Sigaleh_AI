import tensorflow as tf
import joblib

model = tf.keras.models.load_model(
    "model/model_lstm.keras"
)

scaler = joblib.load(
    "model/scaler.save"
)