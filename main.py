import os
import yaml
import subprocess
import argparse

from Courses import courses
from STT import stt
from Utils import utils

#For disabling terminal logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def parse_args():
    parser = argparse.ArgumentParser(description='Arguments and Their Descriptions.')
    parser.add_argument('--native_language_id', default = None,
                        help='An Argument For The Native Language (0 ---> "En" / 1 ---> "Ru").')
    parser.add_argument('--course_language_id', default = None,
                        help='An Argument For The Native Language (0 ---> "En" / 1 ---> "Ru").')
    args = parser.parse_args()
    if (args.native_language_id is None) or (args.course_language_id is None):
            print('Please Specify --native_language_id/--course_language_id Arguments.')
            sys.exit()
    return args

if __name__ == "__main__":
    params = parse_args()
    main_dir = os.getcwd()

    #Load configurations for startup
    config_file_path = os.path.join(main_dir, "config.yaml")
    config_file =  open(config_file_path, 'r+')
    main_config = yaml.safe_load(config_file)

    #Contains languages list and corresponding ID's
    languages = main_config["Languages"]

    #Get startup language ID (En: 0, Ru: 1)
    language = str(params.native_language_id)

    stt_folder = main_config["STT"]["Model Folder"]
    stt_folder = os.path.join(main_dir, stt_folder)

    courses_tts_folder =  main_config["Courses"]["TTS Folder"]
    courses_tts_folder = os.path.join(main_dir, courses_tts_folder)

    courses_data_folder =  main_config["Courses"]["Data Folder"]
    courses_data_folder = os.path.join(main_dir, courses_data_folder)

    courses_collection_folder =  main_config["Courses"]["Saved Data Folder"]
    courses_collection_folder = os.path.join(main_dir, courses_collection_folder)

    #Preprocess voice activity detection and load STT model without scorer
    model_path = os.path.join(stt_folder, params.course_language_id)

    # Start audio with VAD
    vad_audio = stt.VADAudio(aggressiveness = 3, input_rate=16000)

    vad_audio.set_model(model_path, 'model.tflite')
    #vad_audio.set_scorer(model_path, 'conversation.scorer')

    #Start the course
    #Make data collection path for language
    collection_folder = os.path.join(courses_collection_folder, params.course_language_id)
    courses.start_course(os.path.join(courses_tts_folder, params.native_language_id), os.path.join(courses_data_folder, params.native_language_id), vad_audio, stt, model_path, main_config, config_file, collection_folder)

    config_file.close()
