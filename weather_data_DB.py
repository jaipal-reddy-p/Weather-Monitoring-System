from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string if using MongoDB Atlas
db = client['weather_monitoring']  # Create or select the database
raw_weather_collection = db['raw_weather_data']  # Collection for real-time weather data
daily_summary_collection = db['daily_weather_summary']  # Collection for daily summaries

# List of cities to process
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Function to calculate daily summaries for a city
def calculate_daily_summary(city):
    # Get today's date
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)

    # Query weather data for the current day (between midnight and the end of the day)
    weather_data = list(raw_weather_collection.find({
        "city": city,
        "timestamp": {"$gte": today.strftime('%Y-%m-%d %H:%M:%S'), "$lt": tomorrow.strftime('%Y-%m-%d %H:%M:%S')}
    }))
    
    if not weather_data:
        print(f"No data found for {city} on {today.date()}")
        return
    
    # Calculate the average, max, and min temperatures
    temperatures = [data['temp_celsius'] for data in weather_data]
    avg_temp = sum(temperatures) / len(temperatures)
    max_temp = max(temperatures)
    min_temp = min(temperatures)

    # Find the most frequent weather condition (dominant weather condition)
    weather_conditions = [data['weather_condition'] for data in weather_data]
    dominant_weather_condition = max(set(weather_conditions), key=weather_conditions.count)

    # Create a summary object
    daily_summary = {
        "city": city,
        "date": today.strftime('%Y-%m-%d'),
        "avg_temp": avg_temp,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "dominant_weather_condition": dominant_weather_condition
    }

    # Store the daily summary in the database
    daily_summary_collection.insert_one(daily_summary)
    print(f"Daily summary for {city} on {today.strftime('%Y-%m-%d')} stored in MongoDB.")

# Main function to calculate summaries for all cities
def calculate_summaries_for_all_cities():
    for city in cities:
        calculate_daily_summary(city)

if __name__ == "__main__":
    calculate_summaries_for_all_cities()
