import requests
import time
from datetime import datetime
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string if using MongoDB Atlas
db = client['weather_monitoring']  # Create or select the database
raw_weather_collection = db['raw_weather_data']  # Collection for real-time weather data
daily_summary_collection = db['daily_weather_summary']  # Collection for daily summaries

# OpenWeatherMap API Key (replace with your actual key)
API_KEY = "ENTER_YOUR_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"

# List of Indian cities (with their corresponding OpenWeatherMap city names or IDs)
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Function to fetch weather data for a city and store in MongoDB
def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant data
        city_name = data["name"]
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = kelvin_to_celsius(temperature_kelvin)
        feels_like_celsius = kelvin_to_celsius(data["main"]["feels_like"])
        weather_condition = data["weather"][0]["main"]
        timestamp = datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create a structured weather data object
        weather_data = {
            "city": city_name,
            "temp_celsius": temperature_celsius,
            "feels_like_celsius": feels_like_celsius,
            "weather_condition": weather_condition,
            "timestamp": timestamp
        }
        
        # Insert the weather data into MongoDB
        raw_weather_collection.insert_one(weather_data)
        print(f"Weather data for {city} stored in MongoDB.")
        
    else:
        print(f"Error fetching data for {city}: {response.status_code}")

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Main function to continuously fetch and store weather data
def fetch_weather_data():
    while True:
        for city in cities:
            fetch_weather(city)
        
        # Sleep for 5 minutes before fetching data again
        time.sleep(300)  # 300 seconds = 5 minutes

if __name__ == "__main__":
    fetch_weather_data()
