#!/usr/bin/env python3
"""
MQTT Example
Demonstrates publishing sensor data to an MQTT broker.
"""

from wdw_sensors import DHT22, MPU6050
import time
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def main():
    dht22 = DHT22(pin=4)
    mpu6050 = MPU6050()
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("localhost", 1883, 60)
    client.loop_start()
    
    print("MQTT Example")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Read DHT22
            dht_data = dht22.read()
            client.publish("sensors/dht22/temperature", dht_data['temperature'])
            client.publish("sensors/dht22/humidity", dht_data['humidity'])
            
            # Read MPU6050
            mpu_data = mpu6050.read()
            client.publish("sensors/mpu6050/accel/x", mpu_data['accel']['x'])
            client.publish("sensors/mpu6050/gyro/x", mpu_data['gyro']['x'])
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")
        client.loop_stop()

if __name__ == "__main__":
    main()
