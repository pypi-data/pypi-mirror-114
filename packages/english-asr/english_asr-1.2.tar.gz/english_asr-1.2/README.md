# english_asr
An Automatic Speech Recognition (ASR) models in TensorFlow Lite (TFLite) for Speech-To-Text conversion.

## Installation
- pip3 install english-asr

## Supported Model
- [Conformer Transducer](https://arxiv.org/abs/2005.08100) using [LibriSpeech](http://www.openslr.org/12) dataset.

## How To Run
```
from english_asr.conformer import get_text_from_speech
out = get_text_from_speech('audio.wav')```
