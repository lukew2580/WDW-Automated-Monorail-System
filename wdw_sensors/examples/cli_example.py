#!/usr/bin/env python3
"""
CLI Example
Demonstrates using the CLI tool to read sensor data.
"""

import subprocess
import time

def main():
    print("CLI Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Read DHT22
            result = subprocess.run(["wdw-sensor", "read", "dht22", "--pin", "4"], capture_output=True, text=True)
            print(f"DHT22: {result.stdout.strip()}")
            
            # Read MPU6050
            result = subprocess.run(["wdw-sensor", "read", "mpu6050"], capture_output=True, text=True)
            print(f"MPU6050: {result.stdout.strip()}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
