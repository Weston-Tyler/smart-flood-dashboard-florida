# data_ingestion/soil_moisture_ingest.py
from kafka import KafkaProducer
import requests
import json
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Placeholder API Endpoint for Soil Moisture Data
SOIL_MOISTURE_API_URL = "https://api.example.com/soil_moisture"  # Replace with actual endpoint

def fetch_soil_moisture_data():
    response = requests.get(SOIL_MOISTURE_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch soil moisture data: {response.status_code}")
        return None

def produce_soil_moisture_data():
    while True:
        data = fetch_soil_moisture_data()
        if data:
            producer.send('soil_moisture', data)
            print("Sent soil moisture data to Kafka")
        time.sleep(600)  # Fetch data every 10 minutes

if __name__ == "__main__":
    produce_soil_moisture_data()
