import base64
import datetime

import requests
API_KEY = '4e149c02286b07df0fda6d7c04bb8c14'
PRO_KEY = '5a84284e5bc4bf6180fc60f684c915df'


def get_icon_data(icon):
    url = f'http://openweathermap.org/img/wn/{icon}.png'
    response = requests.get(url, stream=True)
    return base64.encodebytes(response.raw.read())


def get_weather(lat, lon):
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}').json()

def get_forecast(lat, lon):
    return requests.get(f'https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=10&units=metric&appid={PRO_KEY}')

def get_3_day_forecast(lat, lon):
    weather = get_forecast(lat, lon).json()
    forecast = [{'date': datetime.datetime.fromtimestamp(d['dt']),
                 'temp': d['temp']['day'],
                 'icon': d['weather'][0]['icon']}for d in weather['list']]
    return forecast[1: 4]




