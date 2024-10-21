from WeatherApp.app.models import WeatherData, DailySummary
from datetime import datetime
from sqlalchemy import func
from WeatherApp.app import db


def convert_kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def calculate_daily_summary(city):
    today = datetime.utcnow().date()

    weather_records = db.session.query(WeatherData).filter(
        WeatherData.city == city,
        func.date(WeatherData.timestamp) == today
    ).all()

    if not weather_records:
        return None

    temperatures = [record.temperature for record in weather_records]
    avg_temp = sum(temperatures) / len(temperatures)
    max_temp = max(temperatures)
    min_temp = min(temperatures)

    dominant_weather = get_dominant_weather(weather_records)

    daily_summary = DailySummary(
        city=city,
        avg_temp=avg_temp,
        max_temp=max_temp,
        min_temp=min_temp,
        dominant_weather=dominant_weather,
        date=today
    )

    db.session.add(daily_summary)
    db.session.commit()

    return {
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'dominant_weather': dominant_weather
    }


def get_dominant_weather(weather_records):
    weather_counts = {}
    for record in weather_records:
        weather = record.weather_condition
        if weather not in weather_counts:
            weather_counts[weather] = 1
        else:
            weather_counts[weather] += 1

    dominant_weather = max(weather_counts, key=weather_counts.get)
    return dominant_weather
