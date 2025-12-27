// WDW Monorail Sensors Library (C++ Header)
#ifndef WDW_SENSORS_HPP
#define WDW_SENSORS_HPP

#include <cstdint>

namespace WDW {

// DHT22
class DHT22 {
public:
    DHT22(int pin);
    ~DHT22();
    
    struct Data {
        float temperature;
        float humidity;
    };
    
    Data read();
    Data read_fast();
    
private:
    int pin;
};

// MPU6050
class MPU6050 {
public:
    MPU6050();
    ~MPU6050();
    
    struct AccelData {
        float x;
        float y;
        float z;
    };
    
    struct GyroData {
        float x;
        float y;
        float z;
    };
    
    struct Data {
        AccelData accel;
        GyroData gyro;
    };
    
    Data read();
    
private:
    void initialize();
};

} // namespace WDW

#endif // WDW_SENSORS_HPP
