# STT-Engine-Dataset-Improver
A tool that allows to improve speech-to-text engine datasets. The tool uses pre-trained models.

### Description
The tool can generate datasets for DeepSpeech speech-to-text engine using a pre-trained DeepSpeech model.
First, the user should listen to the speech in the native language, then the translated variant (translated in the course language). After that, the user should repeat the translated speech. The pre-trained model will validate (optional) the speech and include recorded audio file, validated transcription and file size into CSV file corresponding to the format of DeepSpeech's Common Voice corpus structure.

[DeepSpeech](https://github.com/mozilla/DeepSpeech) is a speech-to-text engine based on [Baidu's Deep Speech research paper](https://arxiv.org/abs/1412.5567). Project DeepSpeech uses datasets provided by Mozilla's other project calling Common Voice.

Audio clips specifications:
  * Audio file format: WAV.
  * Channels number: 1(mono).
  * Sampling rate: 16000 Hz.

The CSV file have the following fields:
  * wav_filename: the path of the sample, either absolute or relative. Here, the importer produces relative paths.
  * wav_filesize: samples size given in bytes, used for sorting the data before training. Expects positive integer.
  * transcript: transcription target for the sample.

An important note is that DeepSpeech can only process audios that are longer than 0.5 seconds, shorter than 20 seconds and are not too short for transcript. The tool checks for these too.

### Environment and Requirements
  * OS: Ubuntu 20.04.
  * Python 3 version: 3.6.9.
  * Pip 3 version: 9.0.1.

Install the required dependencies:
> sudo apt-get install -y mpg321

> sudo apt install python3-pip python3-pyaudio libatlas3-base

> pip3 install -r requirements.txt

### Supported Languages are:
  - [x] English (ID: 0)
  - [x] Russian (ID: 1)

### Run
Input arguments are:
  * --native_language_id: an Argument For The Native Language (0 ---> "En" / 1 ---> "Ru").
  * --course_language_id: an Argument For The Native Language (0 ---> "En" / 1 ---> "Ru").
  * --validation: an Argument For The validation Of Speech With Deepspeech Pre-Trained Model (0 ---> False / 1 ---> True). The Default Value Is 1.

First time run example (collects English audio clips):
> python3 main.py --native_language 1 --course_language 0
