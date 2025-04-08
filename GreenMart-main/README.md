# EchoMart
A shopping app built with Python that uses Face Recognition for login and Speech Recognition for search.
The GUI is entirely built on PyQT5. Face Recognition is built with OpenCV and the face_recognition library.
The Speech-to-Text is handled by OpenAI Whisper which is an open source language model along with SpeechRecognition library in Python.
The search query processing is done using NLTK and some NLP techniques.

# Setup
Install the following for setting the project up
## Dependencies
### [Python 3.9.9](https://www.python.org/downloads/release/python-399/)
### face_recognition and dlib
### [OpenaAI Whisper](https://github.com/openai/whisper)
### PyTorch
### SpeechRecognition
### OpenCV
### PyQT5
### [NLTK](https://www.nltk.org/)
### Pandas
### Numpy

Now download all the files in the repository.
Make folders face_encodings and Profile before runnning for the first time.
EchoMart is now ready.

## Running on GPU (optional)
By default the Whisper model will run on CPU using FP32 (this results in higher latency when using speech recognition)
To use FP16 we must set up the GPU to run CUDA. If CUDA is available on the GPU refer the following:
https://github.com/pytorch/pytorch/issues/90845
