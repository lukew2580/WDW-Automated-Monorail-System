#!/usr/bin/env python3
"""
Advanced Example
Demonstrates advanced usage of the sensors.
"""

from wdw_sensors import DHT22, MPU6050
import time

def main():
    # DHT22 in fast mode
    dht22 = DHT22(pin=4, fast_mode=True)
    
    # MPU6050 with custom address
    mpu6050 = MPU6050(address=0x69)
    
    print("Advanced Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Read DHT22 in fast mode
            dht_data = dht22.read_fast()
            print(f"DHT22: Temperature={dht_data['temperature']}°C, Humidity={dht_data['humidity']}%")
            
            # Read MPU6050
            mpu_data = mpu6050.read()
            print(f"MPU6050: {mpu_data}")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
