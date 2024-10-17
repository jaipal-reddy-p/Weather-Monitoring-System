import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['weather_monitoring']  # Database for weather data
daily_summary_collection = db['daily_weather_summary']  # Collection for daily summaries
alerts_collection = db['alerts']  # Collection for alerts

# Function to visualize temperature trends for a city
def visualize_temperature_trends(city):
    # Query daily summaries for the city
    data = list(daily_summary_collection.find({"city": city}).sort("date", 1))
    
    if not data:
        print(f"No data found for {city}.")
        return
    
    # Extract dates and temperature values
    dates = [entry['date'] for entry in data]
    avg_temps = [entry['avg_temp'] for entry in data]
    min_temps = [entry['min_temp'] for entry in data]
    max_temps = [entry['max_temp'] for entry in data]
    
    # Plot the temperature trends
    plt.figure(figsize=(10, 5))
    plt.plot(dates, avg_temps, label='Average Temp', marker='o', color='b')
    plt.plot(dates, min_temps, label='Min Temp', marker='o', color='g')
    plt.plot(dates, max_temps, label='Max Temp', marker='o', color='r')
    
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Temperature Trends for {city}')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Function to visualize dominant weather conditions for a city
def visualize_dominant_weather(city):
    # Query daily summaries for the city
    data = list(daily_summary_collection.find({"city": city}).sort("date", 1))
    
    if not data:
        print(f"No data found for {city}.")
        return
    
    # Extract weather conditions
    conditions = [entry['dominant_weather_condition'] for entry in data]
    
    # Count the frequency of each condition
    condition_counts = pd.Series(conditions).value_counts()
    
    # Plot the dominant weather conditions
    plt.figure(figsize=(8, 5))
    condition_counts.plot(kind='bar', color='c')
    
    plt.xlabel('Weather Condition')
    plt.ylabel('Frequency')
    plt.title(f'Dominant Weather Conditions for {city}')
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Function to visualize alert history
def visualize_alert_history():
    # Query all alerts
    alerts = list(alerts_collection.find().sort("timestamp", 1))
    
    if not alerts:
        print("No alerts found.")
        return
    
    # Extract alert data
    cities = [alert['city'] for alert in alerts]
    timestamps = [alert['timestamp'] for alert in alerts]
    messages = [alert['alert_message'] for alert in alerts]
    
    # Plot alerts over time
    plt.figure(figsize=(12, 6))
    plt.bar(timestamps, range(len(timestamps)), color='r')
    
    plt.xlabel('Time')
    plt.ylabel('Alerts Triggered')
    plt.title('Alert History')
    plt.xticks(rotation=45)
    
    # Display alert messages with the time
    for i, (time, message) in enumerate(zip(timestamps, messages)):
        plt.text(time, i, message, fontsize=9, rotation=45, ha='right')

    # Show the plot
    plt.tight_layout()
    plt.show()

# Main function to choose visualization options
def main():
    print("Choose a visualization:")
    print("1. Temperature Trends for a City")
    print("2. Dominant Weather Conditions for a City")
    print("3. Alert History")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        city = input("Enter city name: ").strip()
        visualize_temperature_trends(city)
    elif choice == "2":
        city = input("Enter city name: ").strip()
        visualize_dominant_weather(city)
    elif choice == "3":
        visualize_alert_history()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
