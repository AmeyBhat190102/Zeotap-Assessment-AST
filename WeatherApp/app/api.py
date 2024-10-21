import requests
from WeatherApp.app.config import OPENWEATHER_API_KEY

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
