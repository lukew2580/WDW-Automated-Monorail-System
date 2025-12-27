# WDW Monorail Sensors Library

A unified library for interacting with sensors in the WDW Monorail System.

## Quick Start

### Installation
```bash
pip install wdw-sensors
```

### Usage
```python
from wdw_sensors import DHT22, MPU6050

# Read DHT22
dht22 = DHT22(pin=4)
data = dht22.read()
print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")

# Read MPU6050
mpu6050 = MPU6050()
data = mpu6050.read()
print(f"Acceleration: {data['accel']}, Gyro: {data['gyro']}")
```

## Advanced Usage

### Fast Mode
```python
dht22 = DHT22(pin=4, fast_mode=True)
data = dht22.read_fast()
```

### Custom I2C Address
```python
mpu6050 = MPU6050(address=0x69)
data = mpu6050.read()
```

## Wiring

### DHT22
```
DHT22 DATA → Raspberry Pi GPIO4 (Pin 7)
DHT22 VCC → 3.3V (Pin 1)
DHT22 GND → GND (Pin 6)
```

### MPU6050
```
MPU6050 SDA → Raspberry Pi SDA (Pin 3)
MPU6050 SCL → Raspberry Pi SCL (Pin 5)
MPU6050 VCC → 3.3V (Pin 1)
MPU6050 GND → GND (Pin 6)
```

## Examples

See the [examples](examples/) directory for more usage examples.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License. See [LICENSE](LICENSE) for details.
