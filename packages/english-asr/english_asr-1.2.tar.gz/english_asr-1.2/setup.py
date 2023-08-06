import pip
from setuptools import find_packages, setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='english_asr',
    version='1.2',
    author="Neha Soni",
    author_email = 'soni.neha45@gmail.com',
    url = 'https://github.com/neso613/english_asr',
    description="An Automatic Speech Recognition(ASR) for English language trained on LibriSpeech dataset using Conformer.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache-2.0",
    packages=['english_asr'],
    include_package_data=True,
    package_data={
        'conformer': ['conformer.tflite'],
    },
    python_requires=">=3.5",
    install_requires=[
        "librosa",
        "tensorflow",
        "soundfile>=0.10.2",
    ]
)
