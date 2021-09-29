import os
import yaml
from Utils import utils

#Check checkpoint
#Checkpoint must be in range of (0, len(numbers_keys_list) + len(converstaion_keys_list))
def check_checkpoint_limit(all_commands_number, course_language_id, config_file_data, config_file):
    current_command_id = utils.load_course_checkpoint(course_language_id, config_file_data)
    if current_command_id == all_commands_number:
        utils.save_course_checkpoint(course_language_id, 0, config_file_data, config_file)

def get_answer(stt, vad_audio, correct_answer, numbers_speech, repeat_speech, again_repeat_speech, excellent_speech, current_command_id, collection_folder):
    while True:
        file_name = str()
        file_size = str()
        answer, file_name, file_size = stt.listen_audio(vad_audio, save_wav = True, save_wav_path = collection_folder)
        if answer == '':
            #Remove saved wav file
            os.remove(file_name)
            continue
        if answer != '' and len(answer) > 0 and answer != correct_answer:
            #Remove saved wav file
            os.remove(file_name)
            utils.load_play_tts_clip(again_repeat_speech)
            utils.play_tts_clip(numbers_speech)
            utils.load_play_tts_clip(repeat_speech)
            continue
        else:
            #Update command id
            current_command_id+=1
            #Play speech
            utils.load_play_tts_clip(excellent_speech)
            return current_command_id, file_name, file_size

def start_course(courses_tts_folder, courses_data_folder, vad_audio, stt, model_path, config_file_data, config_file, collection_folder):
    #Load course id from config checkpoint
    #model_path contains the id of course language
    course_language_id = os.path.basename(model_path)
    current_command_id = utils.load_course_checkpoint(course_language_id, config_file_data)

    #Load YAML file that contains translation pairs with corresponding ID's
    data_file =  open(os.path.join(courses_data_folder, "data.yaml"), 'r')
    data_file_yaml = yaml.full_load(data_file)
    #Configure TTS speech audio clips paths
    #courses_tts_folder is a full path and contains language ID too
    numbers_course_prespeech = os.path.join(courses_tts_folder, "0")
    conversation_course_prespeech = os.path.join(courses_tts_folder, "2")
    numbers_speech = os.path.join(courses_tts_folder, "1")
    conversation_speech = os.path.join(courses_tts_folder, "3")
    repeat_speech = os.path.join(courses_tts_folder, "4")
    again_repeat_speech = os.path.join(courses_tts_folder, "5")
    course_continue_speech = os.path.join(courses_tts_folder, "6")
    excellent_speech = os.path.join(courses_tts_folder, "7")

    #Get the data. Each line index of data correspondes to the ID of .mp3 clip
    numbers_data = data_file_yaml.get("Numbers")
    conversation_data = data_file_yaml.get("Conversation")

    #Make list of keys of number data
    numbers_keys_list = list(numbers_data)
    #Make list of keys of conversation data
    conversation_keys_list = list(conversation_data)

    #Check course current status
    if current_command_id == 0:
        utils.load_play_tts_clip(numbers_course_prespeech)
    elif current_command_id == len(numbers_keys_list):
        utils.load_play_tts_clip(conversation_course_prespeech)
    else:
        utils.load_play_tts_clip(course_continue_speech)

    #Check for resuming course from numbers
    if current_command_id < len(numbers_keys_list):
        #Load numbers scorer
        vad_audio.set_scorer(model_path, 'course_numbers.scorer')
        for i in range(current_command_id, len(numbers_keys_list)):
            utils.play_tts_clip(os.path.join(numbers_speech, str(i) + ".mp3"))
            utils.load_play_tts_clip(repeat_speech)
            #Get expected answer line from numbers data dictionary
            correct_answer = numbers_data.get(numbers_keys_list[i])
            #Load current number speech
            current_number_speech = os.path.join(numbers_speech, str(i) + ".mp3")
            current_command_id, file_name, file_size = get_answer(stt, vad_audio, correct_answer, current_number_speech, repeat_speech, again_repeat_speech, excellent_speech, current_command_id, collection_folder)
            #Check for audio length and update csv
            if utils.check_audio(correct_answer, file_name, file_size):
                #Update collected data in csv
                utils.write_to_csv(file_name, file_size, correct_answer, collection_folder)
            else:
                os.remove(file_name)
            #Save the checkpoint in config
            utils.save_course_checkpoint(course_language_id, current_command_id, config_file_data, config_file)
    else:
        #Load commands scorer
        vad_audio.set_scorer(model_path, 'course_commands.scorer')
        for i in range(current_command_id - len(numbers_keys_list), len(conversation_keys_list)):
            utils.play_tts_clip(os.path.join(conversation_speech, str(i) + ".mp3"))
            utils.load_play_tts_clip(repeat_speech)
            #Get expected answer line from conversation data dictionary
            correct_answer = conversation_data.get(conversation_keys_list[i])
            #Load current command speech
            current_command_speech = os.path.join(conversation_speech, str(i) + ".mp3")
            current_command_id, file_name, file_size = get_answer(stt, vad_audio, correct_answer, current_command_speech, repeat_speech, again_repeat_speech, excellent_speech, current_command_id, collection_folder)
            #Check for audio length and update csv
            if utils.check_audio(correct_answer, file_name, file_size):
                #Update collected data in csv
                utils.write_to_csv(file_name, file_size, correct_answer, collection_folder)
            else:
                os.remove(file_name)
            #Save the checkpoint in config
            utils.save_course_checkpoint(course_language_id, current_command_id, config_file_data, config_file)
    check_checkpoint_limit(len(numbers_keys_list) + len(conversation_keys_list), course_language_id, config_file_data, config_file)
