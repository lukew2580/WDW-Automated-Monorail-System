// C++ Example
// Demonstrates using the C++ library to read sensor data.

#include <iostream>
#include <unistd.h>
#include "wdw_sensors.hpp"

int main() {
    WDW::DHT22 dht22(4);
    WDW::MPU6050 mpu6050;
    
    std::cout << "C++ Example" << std::endl;
    std::cout << "Press Ctrl+C to exit" << std::endl;
    
    while (true) {
        // Read DHT22
        auto dht_data = dht22.read();
        std::cout << "DHT22: Temperature=" << dht_data.temperature << "°C, Humidity=" << dht_data.humidity << "%" << std::endl;
        
        // Read MPU6050
        auto mpu_data = mpu6050.read();
        std::cout << "MPU6050: Accel X=" << mpu_data.accel.x << ", Gyro X=" << mpu_data.gyro.x << std::endl;
        
        sleep(2);
    }
    
    return 0;
}
