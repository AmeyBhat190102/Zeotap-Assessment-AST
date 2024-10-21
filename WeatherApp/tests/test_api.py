import unittest
from WeatherApp.app.api import get_weather_data

class TestWeatherAPI(unittest.TestCase):
    def test_get_weather_data(self):
        data = get_weather_data('Mumbai')
        self.assertIsNotNone(data)
        self.assertIn('main', data)

if __name__ == '__main__':
    unittest.main()
