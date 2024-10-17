import unittest
from pymongo import MongoClient
from weather_data_fetcher import fetch_weather, kelvin_to_celsius

class TestWeatherSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup MongoDB connection
        cls.client = MongoClient('mongodb://localhost:27017/')
        cls.db = cls.client['weather_monitoring']
        cls.raw_weather_collection = cls.db['raw_weather_data']
    
    def test_kelvin_to_celsius(self):
        # Test temperature conversion
        kelvin_temp = 300.15
        expected_celsius = 27.0
        self.assertEqual(kelvin_to_celsius(kelvin_temp), expected_celsius)
    
    def test_fetch_weather(self):
        # Test fetching weather data for a city
        city = "Delhi"
        weather_data = fetch_weather(city)
        self.assertIsNotNone(weather_data)
        self.assertIn('city', weather_data)
        self.assertIn('temp_celsius', weather_data)
        self.assertEqual(weather_data['city'], city)
    
    def test_weather_data_storage(self):
        # Ensure that weather data is stored in MongoDB
        city = "Delhi"
        weather_data = fetch_weather(city)
        self.raw_weather_collection.insert_one(weather_data)
        stored_data = self.raw_weather_collection.find_one({"city": city})
        self.assertIsNotNone(stored_data)
        self.assertEqual(stored_data['city'], city)

    @classmethod
    def tearDownClass(cls):
        # Cleanup test data from MongoDB
        cls.raw_weather_collection.delete_many({"city": "Delhi"})

if __name__ == '__main__':
    unittest.main()
