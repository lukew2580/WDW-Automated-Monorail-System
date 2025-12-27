// C Example
// Demonstrates using the C library to read sensor data.

#include <stdio.h>
#include <unistd.h>
#include "wdw_sensors.h"

int main() {
    DHT22 dht22 = dht22_init(4);
    MPU6050 mpu6050 = mpu6050_init();
    
    printf("C Example\n");
    printf("Press Ctrl+C to exit\n");
    
    while (1) {
        // Read DHT22
        DHT22Data dht_data = dht22_read(dht22);
        printf("DHT22: Temperature=%.2f°C, Humidity=%.2f%%\n", dht_data.temperature, dht_data.humidity);
        
        // Read MPU6050
        MPU6050Data mpu_data = mpu6050_read(mpu6050);
        printf("MPU6050: Accel X=%.2f, Gyro X=%.2f\n", mpu_data.accel.x, mpu_data.gyro.x);
        
        sleep(2);
    }
    
    return 0;
}
