import pip
from setuptools import find_packages, setup
setup(
    name='english_asr',
    version='1.1',
    author="Neha Soni",
    author_email = 'soni.neha45@gmail.com',
    url = 'https://github.com/neso613/english_asr',
    description="An Automatic Speech Recognition(ASR) for English language trained on LibriSpeech dataset using Conformer.",
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
