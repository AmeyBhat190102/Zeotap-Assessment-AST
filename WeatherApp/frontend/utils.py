import requests

API_BASE_URL = "http://127.0.0.1:5000/weather/summary"
ALERTS_BASE_URL = "http://127.0.0.1:5000/alerts"
THRESHOLDS_BASE_URL = "http://127.0.0.1:5000/set_threshold"

def get_city_weather_summary(city):
    try:
        response = requests.get(f"{API_BASE_URL}/{city}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None

def get_alerts(city):
    try:
        response = requests.get(f"{ALERTS_BASE_URL}/{city}")
        if response.status_code == 200:
            return response.json().get('alerts', [])
    except Exception as e:
        return []

def set_thresholds(threshold):
    try:
        requests.post(THRESHOLDS_BASE_URL, json={"threshold": threshold})
    except Exception as e:
        pass
