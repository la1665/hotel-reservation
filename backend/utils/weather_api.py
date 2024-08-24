import requests
import json

from settings import settings


def get_weather_for_city(city: str, api_key: str = settings.WEATHER_API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city.capitalize()},IR&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        return result.get("weather")
    else:
        return None
