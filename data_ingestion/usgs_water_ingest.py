# data_ingestion/usgs_water_ingest.py
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

# Define USGS Water Services API Endpoint and Parameters
USGS_API_URL = "https://waterservices.usgs.gov/nwis/iv/"
PARAMS = {
    'format': 'json',
    'sites': '02210000,02210001',  # Example site codes for Florida rivers/bays
    'parameterCd': '00060,00065',  # Discharge (00060) and gage height (00065)
    'siteStatus': 'all'
}

def fetch_water_data():
    response = requests.get(USGS_API_URL, params=PARAMS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch water data: {response.status_code}")
        return None

def produce_water_data():
    while True:
        data = fetch_water_data()
        if data:
            producer.send('water_levels', data)
            print("Sent water levels data to Kafka")
        time.sleep(300)  # Fetch data every 5 minutes

if __name__ == "__main__":
    produce_water_data()


