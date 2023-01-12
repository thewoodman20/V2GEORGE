import requests
import datetime as dt

def weather():
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = ""
    LATITUDE = "40.7128"
    LONGITUDE = "74.0060"
    url = BASE_URL + "lat=" + LATITUDE + "&lon=" + LONGITUDE + "&appid=" + API_KEY
    response = requests.get(url).json()
    print(response)