#!/usr/bin/env python3
"""
Visualization Example
Demonstrates visualizing sensor data using matplotlib.
"""

from wdw_sensors import DHT22, MPU6050
import time
import matplotlib.pyplot as plt

def main():
    dht22 = DHT22(pin=4)
    mpu6050 = MPU6050()
    
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    temperature_data = []
    humidity_data = []
    
    print("Visualization Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Read DHT22
            dht_data = dht22.read()
            temperature_data.append(dht_data['temperature'])
            humidity_data.append(dht_data['humidity'])
            
            # Update plots
            ax1.clear()
            ax1.plot(temperature_data, label='Temperature (°C)')
            ax1.plot(humidity_data, label='Humidity (%)')
            ax1.legend()
            ax1.set_title('DHT22 Data')
            
            # Read MPU6050
            mpu_data = mpu6050.read()
            ax2.clear()
            ax2.plot(mpu_data['accel']['x'], label='Accel X')
            ax2.plot(mpu_data['gyro']['x'], label='Gyro X')
            ax2.legend()
            ax2.set_title('MPU6050 Data')
            
            plt.pause(0.1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
