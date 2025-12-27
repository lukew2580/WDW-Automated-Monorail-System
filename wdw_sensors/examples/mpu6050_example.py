#!/usr/bin/env python3
"""
MPU6050 Example
Demonstrates reading accelerometer and gyroscope data.
"""

from wdw_sensors import MPU6050
import time

def main():
    sensor = MPU6050()
    
    print("MPU6050 Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            data = sensor.read()
            print(f"Acceleration: {data['accel']}, Gyro: {data['gyro']}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
