#!/usr/bin/env python3
"""
DHT22 Example
Demonstrates reading temperature and humidity data.
"""

from wdw_sensors import DHT22
import time

def main():
    sensor = DHT22(pin=4)
    
    print("DHT22 Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            data = sensor.read()
            print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
