# coding: utf-8
import tensorflow as tf
import librosa
import os
import numpy as np

tflite_model = 'english_asr/conformer.tflite'
interpreter = tf.lite.Interpreter(model_path=tflite_model)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("\n-----Conformer ASR-TFLite model loaded-----\n")

def get_text_from_speech(input_wav):
    signal, _ = librosa.load(os.path.expanduser(input_wav), sr=16000, mono=True)
    interpreter.resize_tensor_input(input_details[0]["index"], signal.shape)
    interpreter.allocate_tensors()
    interpreter.set_tensor(input_details[0]["index"], signal)
    interpreter.set_tensor(
    input_details[1]["index"],
    np.array(0).astype('int32')
    )
    interpreter.set_tensor(
    input_details[2]["index"],
    np.zeros([1,2,1,320]).astype('float32')
    )
    interpreter.invoke()
    hyp = interpreter.get_tensor(output_details[0]["index"])
    out = "".join([chr(u) for u in hyp])
    return out
