import requests
import time
from datetime import datetime

# OpenWeatherMap API Key (replace with your actual key)
API_KEY = "febe2e04dd38c33de33887afdee24f7f"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"

# List of Indian cities (with their corresponding OpenWeatherMap city names or IDs)
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Function to fetch weather data for a city
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
        return weather_data
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Main function to continuously fetch weather data
def fetch_weather_data():
    while True:
        for city in cities:
            weather_data = fetch_weather(city)
            if weather_data:
                print(weather_data)  # For now, just print the data; later we will store it in a database.
            
        # Sleep for 5 minutes before fetching data again
        time.sleep(300)

if __name__ == "__main__":
    fetch_weather_data()
