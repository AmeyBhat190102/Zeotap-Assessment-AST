from apscheduler.schedulers.background import BackgroundScheduler
from WeatherApp.app.api import get_weather_data
from WeatherApp.app.models import WeatherData
from WeatherApps.app import db
from datetime import datetime

def fetch_weather_data_periodically():
    cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            temperature = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            weather_condition = weather_data['weather'][0]['main']
            timestamp = datetime.utcfromtimestamp(weather_data['dt'])

            record = WeatherData(
                city=city,
                temperature=temperature,
                feels_like=feels_like,
                weather_condition=weather_condition,
                timestamp=timestamp
            )
            db.session.add(record)
            db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_weather_data_periodically, 'interval', minutes=5)
scheduler.start()
