# data_ingestion/weather_ingest.py
from kafka import KafkaProducer
import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define OpenWeatherMap API Endpoint and Parameters
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
LOCATION = "Miami,FL"

def fetch_weather_data():
    params = {
        'q': LOCATION,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data: {response.status_code}")
        return None

def produce_weather_data():
    while True:
        data = fetch_weather_data()
        if data:
            producer.send('weather', data)
            print("Sent weather data to Kafka")
        time.sleep(600)  # Fetch data every 10 minutes

if __name__ == "__main__":
    produce_weather_data()
