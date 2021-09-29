import os
import time
import random
import subprocess
import yaml
import csv

#Load course checkpoint in YAML file
def load_course_checkpoint(course_language_id, yaml_file_data):
    checkpoint = int()
    if course_language_id == "0":
        checkpoint = yaml_file_data["Courses"]["Checkpoint English"]
    if course_language_id == "1":
        checkpoint = yaml_file_data["Courses"]["Checkpoint Russian"]
    return checkpoint

#Save course checkpoint in YAML file
def save_course_checkpoint(course_language_id, checkpoint, yaml_file_data, yaml_file):
    if course_language_id == "0":
        yaml_file_data["Courses"]["Checkpoint English"] = checkpoint
    if course_language_id == "1":
        yaml_file_data["Courses"]["Checkpoint Russian"] = checkpoint

    #Reset file pointer and clear YAML config file
    yaml_file.seek(0)
    yaml_file.truncate(0) #Need '0' when using r+
    #Rewrite YAML file content with modified language
    yaml.dump(yaml_file_data, yaml_file, default_flow_style=False, sort_keys=False)

#Function to load and play all or one random or a specific tts clip from directory
def load_play_tts_clip(tts_folder, specific = None, stop_time = 1):
    #Timer for a short stop befor speech
    time.sleep(int(stop_time))
    if specific is not None:
        play = os.path.join(tts_folder, specific + ".mp3")
        p = subprocess.Popen(["mpg321", play, "--stereo"])
        p.wait()
    else:
        all_files = []
        for file in os.listdir(tts_folder):
            if file.endswith(".mp3"):
                all_files.append(os.path.join(tts_folder, file))
        play = random.choice(all_files)
        p = subprocess.Popen(["mpg321", play, "--stereo"])
        p.wait()

#Function to play a clip
def play_tts_clip(clip_path, stop_time = 1):
    #Timer for a short stop befor speech
    time.sleep(int(stop_time))
    p = subprocess.Popen(["mpg321", clip_path, "--stereo"])
    p.wait()

def write_to_csv(file_name, file_size, transcription, output_folder):
    validated_file_path = os.path.join(output_folder, 'validated.csv')

    if os.path.isfile(validated_file_path):
        with open(validated_file_path, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            csvwriter.writerow([os.path.basename(file_name), str(file_size), transcription])
    else:
        csv_header = ['wav_filename','wav_filesize','transcript']
        with open(validated_file_path, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter = ',')
            csvwriter.writerow(csv_header)
            csvwriter.writerow([os.path.basename(file_name), str(file_size), transcription])

    return validated_file_path

#Remove Audios That Are Shorter Than 0.5 Seconds And Longer Than 20 Seconds
#Remove Audios That Are Too Short For Transcript
def check_audio(transcript, file, size):
    if ((size / 32000) > 0.5 and (size / 32000) < 20 and transcript != "" and size / len(transcript) > 1400):
        return True
    else:
        return False
