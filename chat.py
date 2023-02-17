import random
import json
import torch
from model import NeuralNet
from main import bag_of_words, tokenize
import pyttsx3
import speech_recognition as sr
from apps import timer, rng, music, search, weather

def parse_request():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Interpreting...")
            user_input = r.recognize_google(audio, language='en-in')
            print(f"You said: {user_input}")
        except Exception as e:
            print(e)
            pas("Say that again sir")
            return "None"
        return user_input
            
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # [0] for male, [1] for female voice
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()
    
def pas(output):  #print and speak function
    print(output)
    speak(output)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Vgeorge"
pas("Hello sir, how may I be of service?")

def applications(request):
    if "timer" in response:
        timer.timer(request)
    elif "rng" in response:
        rng.rng(request)
    elif "coin" in response:
        rng.coin(request)
    elif "roll_dice" in response:
        rng.dice(request)
    elif "classy_music" in response:
        music.classy_music(request)
    elif "music" in response:
        music.music(request)
    elif "search" in response:
        search.search(request)
    elif "weather" in response:
       weather.weather(request)
    else:
        pass

while True:
    user_input = parse_request()
    if "quit" in user_input or "leave" in user_input or "exit" in user_input:
        break
    
    user_input = tokenize(user_input)
    x = bag_of_words(user_input, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)   #bag of words function returns a numpy array

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() >0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                response = random.choice(intent["responses"])
                if "function" in response:
                    applications(user_input)
                else:
                    print(f'{bot_name}: {response}')
                    speak(response)
    else:
        print(f'{bot_name}: I do not understand...')
