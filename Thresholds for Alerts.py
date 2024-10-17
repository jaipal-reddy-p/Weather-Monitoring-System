import requests
import time
from datetime import datetime
from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['weather_monitoring']  # Database for weather data
raw_weather_collection = db['raw_weather_data']  # Collection for real-time weather data
alerts_collection = db['alerts']  # Collection to store triggered alerts

# OpenWeatherMap API Key
API_KEY = "febe2e04dd38c33de33887afdee24f7f"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API_KEY}"

# List of cities
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# User-configurable thresholds for alerts
thresholds = {
    "temp_threshold": 35,  # Temperature threshold (in Celsius)
    "weather_conditions": ["Storm", "Heavy Rain"]  # Specific weather conditions to trigger alerts
}

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
        weather_condition = data["weather"][0]["main"]
        timestamp = datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create a structured weather data object
        weather_data = {
            "city": city_name,
            "temp_celsius": temperature_celsius,
            "weather_condition": weather_condition,
            "timestamp": timestamp
        }
        
        # Insert weather data into MongoDB
        raw_weather_collection.insert_one(weather_data)
        
        # Check if any thresholds are breached and trigger alerts
        check_alerts(weather_data)
        
        return weather_data
    else:
        print(f"Error fetching data for {city}: {response.status_code}")
        return None

# Function to check if any thresholds are breached and trigger alerts
def check_alerts(weather_data):
    temp = weather_data["temp_celsius"]
    weather_condition = weather_data["weather_condition"]
    
    # Check if temperature exceeds the threshold
    if temp > thresholds["temp_threshold"]:
        trigger_alert(f"Temperature in {weather_data['city']} exceeded {thresholds['temp_threshold']}°C! Current temp: {temp}°C", weather_data)
    
    # Check if the weather condition matches any of the specified conditions
    if weather_condition in thresholds["weather_conditions"]:
        trigger_alert(f"Weather alert in {weather_data['city']}! Condition: {weather_condition}", weather_data)

# Function to trigger an alert (print to console and store in MongoDB)
def trigger_alert(message, weather_data):
    print(f"ALERT: {message}")
    
    # Store the alert in MongoDB
    alert = {
        "city": weather_data["city"],
        "alert_message": message,
        "timestamp": weather_data["timestamp"]
    }
    alerts_collection.insert_one(alert)

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

# Main function to continuously fetch and monitor weather data
def monitor_weather():
    while True:
        for city in cities:
            fetch_weather(city)
        
        # Sleep for 5 minutes before fetching data again
        time.sleep(300)

if __name__ == "__main__":
    monitor_weather()
