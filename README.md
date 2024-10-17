
###Weather Monitoring System

# Weather Monitoring System

## Overview
This is a real-time weather monitoring application that fetches data from the OpenWeatherMap API, processes the data into daily summaries, triggers alerts based on thresholds, and provides visualizations.

## Features
- Fetches real-time weather data for multiple cities.
- Aggregates daily weather summaries (min/max/avg temperature).
- Triggers alerts based on user-defined thresholds.
- Visualizes daily summaries and alerts using graphs.

## Technologies Used
- Python
- MongoDB (for data storage)
- Matplotlib (for visualizations)
- OpenWeatherMap API

## Getting Started

### Prerequisites
- Python 3.x installed
- MongoDB installed and running locally
- Install required Python packages:
  ```bash
  pip install -r requirements.txt

##Get your OpenWeatherMap API key

##Repository Setup
  Clone the GitHub repository:

  git clone https://github.com/jaipal-reddy-p/weather-monitoring-app.git
  cd weather-monitoring-app

##Initialize the Git repository:

  git init
  git remote add origin https://github.com/yourusername/weather-monitoring-app.git

##How to Run the Application
1. Run the Weather Data Fetcher
This script fetches weather data every 5 minutes for multiple cities and stores it in MongoDB.
  python weather_data_fetcher.py

2. Run the Daily Summary Aggregator
This script aggregates daily weather summaries at the end of each day.
  python daily_summary_calculator.py

3. View Visualizations
This script allows you to visualize temperature trends, weather conditions, and alerts.
  python weather_visualizer.py

##Example Visualizations
  Temperature Trends: Shows daily min/max/avg temperatures for a city.
  Dominant Weather Conditions: Bar chart showing the frequency of weather conditions.
  Alert History: Displays triggered alerts over time.

###Cron Jobs for Scheduling
To run the weather fetcher every 5 minutes and the daily summary aggregator at midnight, set up cron jobs:

*/5 * * * * /path/to/python /path/to/weather_data_fetcher.py
0 0 * * * /path/to/python /path/to/daily_summary_calculator.py

#Testing
Unit tests are located in the tests/ directory.
Run the tests:
  python -m unittest discover -s tests

##Non-Functional Aspects
  Security: Implement API key restrictions for OpenWeatherMap.
  Performance: Use MongoDB indexes on timestamp and city fields to optimize data retrieval.
  Error Handling: Handles API errors, invalid responses, and stores error logs.
