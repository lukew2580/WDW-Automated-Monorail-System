#!/usr/bin/env python3
"""
API Example
Demonstrates using the FastAPI server to read sensor data.
"""

import requests
import time

def main():
    print("API Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Read DHT22
            response = requests.get("http://localhost:8000/sensors/dht22")
            print(f"DHT22: {response.json()}")
            
            # Read MPU6050
            response = requests.get("http://localhost:8000/sensors/mpu6050")
            print(f"MPU6050: {response.json()}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
