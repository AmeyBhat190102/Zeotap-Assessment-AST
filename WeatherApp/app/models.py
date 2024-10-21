from sqlalchemy import Column, Integer, Float, String, DateTime
from WeatherApp.app import db

class WeatherData(db.Model):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    weather_condition = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)

class DailySummary(db.Model):
    __tablename__ = 'daily_summary'

    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    avg_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_temp = Column(Float, nullable=False)
    dominant_weather = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
