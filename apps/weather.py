import requests
import datetime as dt
import utils
from geopy.geocoders import Nominatim
import speech_recognition as sr
import json


def parse_request():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Interpreting...")
            locator = r.recognize_google(audio, language='en-in')
            print(f"You said: {locator}")
        except Exception as e:
            print(e)
            utils.pas("Say that again sir")
            return "None"
        return locator

def weather(request):
    weather_request = request
    if "in" in weather_request:
        x = weather_request.index("in")
        while int(x) != -1:
            del(weather_request[0])
            x -= 1
        with open("email.txt", "r") as f:
            email = f.read()
        geolocator = Nominatim(user_agent=email)
        location = geolocator.geocode(weather_request)  #initialize locator and find the location
    else:
        with open("email.txt", "r") as f:
            email = f.read()
        geolocator = Nominatim(user_agent=email)
        with open("config2.json", "r") as f:
            configlocation = json.load(f)
        location = geolocator.geocode(configlocation["Location"])
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    with open("api_key.txt", "r") as f:
        API_KEY = f.read()
    LATITUDE = str(location.latitude)
    LONGITUDE = str(location.longitude)
    url = BASE_URL + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&appid=" + API_KEY
    response = requests.get(url).json()
    temp = round((int(response['main']['temp']) - 273.15)* 9/5 + 32,0)
    location = response['name']
    utils.pas(str(f'it is {temp} degrees fahrenheit outside in {location}'))
    weather = (response['weather'][0]['main']).lower()
    description = response['weather'][0]['description']
    if weather == "clouds":
        utils.pas(str(f"It's also cloudy outside, with some {description} today"))
    elif weather == "clear":
        if description == "clear sky":
            utils.pas(str(f"It's also clear outside, with clear skies today"))
    elif weather == "rain":
        utils.pas(str(f"It's also raining today, {description}"))
    elif weather == "fog":
        utils.pas(str(f"It's foggy today, expect {description}"))
    elif weather == "mist":
        utils.pas(str(f"It's misty outside today"))
    else:
        utils.pas(str(['weather']))


#implement weather by day example "whats the weather like on tuesday"


#{'coord': {'lon': 74.006, 'lat': 40.7128}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02n'}], 'base': 'stations',
# 'main': {'temp': 235.45, 'feels_like':9}, 'clouds': {'all': 11}, 'dt': 1673554929, 'sys': {'country': 'KG', 'sunrise': 1673576805, 'sunset': 1673611061}, 
# 'timezone': 21600, 'id': 8145969, 'name': 'Kara-Kulja', 'cod': 200} 

# 40.7128, -74.0060

#def weather():
#have a default location the weather pulls from 
#whats the weather like in XYZ 
#loop through each word after in and concatenate it in a new variable to be input into the geopy lib
