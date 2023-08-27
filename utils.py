from gtts import gTTS
from playsound import playsound
import json

def speak(audio):
    speech = gTTS(audio)
    with open('speech.mp3', 'wb') as f:
        speech.write_to_fp(f)
        
    with open("config2.json", "r") as f:
        speech_file_path = json.load(f)
    playsound(speech_file_path["Speech File"]) #need to define the file path for the audio

def pas(output):  #print and speak function
    print(output)
    speak(output)