# english_asr
A pip wheel for custom AI model

An Automatic Speech Recognition (ASR) models in TensorFlow Lite (TFLite) for TensorFlow 2.x. We provide end-to-end Jupyter Notebooks that show the inference process using TFLite.

## Installation
- tensorflow
- numpy
- librosa

## Models
- [Conformer Transducer](https://arxiv.org/abs/2005.08100) using [LibriSpeech](http://www.openslr.org/12) dataset.

## How To Run
```
from english_asr.conformer import get_text_from_speech/
out = get_text_from_speech('audio.wav')
