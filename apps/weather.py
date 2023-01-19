import requests
import datetime as dt
import json
import pyttsx3

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

def weather():
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    with open("api_key.txt", "r") as f:
        API_KEY = f.read()
    LATITUDE = "47.5556"
    LONGITUDE = "102.7453"
    url = BASE_URL + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&appid=" + API_KEY
    response = requests.get(url).json()
    temp = round((int(response['main']['temp']) - 273.15)* 9/5 + 32,0)
    location = response['name']
    pas(f'it is {temp} degrees fahrenheit outside in {location}')
    weather = (response['weather'][0]['main']).lower()
    description = response['weather'][0]['description']
    print(weather)
    print(description)
    if weather == "clouds":
        pas(f"It's also cloudy outside, with some {description} today")
    elif weather == "clear":
        pas(f"It's also clear outside, with {description} today")
    elif weather == "rain":
        pas(f"It's also raining today, {description}")
    elif weather == "fog":
        pas(f"It's foggy today, expect {description}")
    else:
        pas(response['weather'])

weather()

#{'coord': {'lon': 74.006, 'lat': 40.7128}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations',
# 'main': {'temp': 235.45, 'feels_like':9}, 'clouds': {'all': 11}, 'dt': 1673554929, 'sys': {'country': 'KG', 'sunrise': 1673576805, 'sunset': 1673611061}, 
# 'timezone': 21600, 'id': 8145969, 'name': 'Kara-Kulja', 'cod': 200} 

# 40.7128, -74.0060