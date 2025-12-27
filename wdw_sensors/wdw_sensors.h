// WDW Monorail Sensors Library (C Header)
#ifndef WDW_SENSORS_H
#define WDW_SENSORS_H

#include <stdint.h>

// DHT22
typedef struct {
    float temperature;
    float humidity;
} DHT22Data;

typedef void* DHT22;

DHT22 dht22_init(int pin);
DHT22Data dht22_read(DHT22 sensor);
void dht22_free(DHT22 sensor);

// MPU6050
typedef struct {
    float x;
    float y;
    float z;
} AccelData;

typedef struct {
    float x;
    float y;
    float z;
} GyroData;

typedef struct {
    AccelData accel;
    GyroData gyro;
} MPU6050Data;

typedef void* MPU6050;

MPU6050 mpu6050_init();
MPU6050Data mpu6050_read(MPU6050 sensor);
void mpu6050_free(MPU6050 sensor);

#endif // WDW_SENSORS_H
