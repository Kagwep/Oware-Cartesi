import tensorflow as tf

model = tf.keras.models.load_model("/home/kagwe/sunoduprojects/oware-game/oware-agent/model/oware-100.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tfmodel = converter.convert()

open("model.tflite" , "wb").write(tfmodel)
     