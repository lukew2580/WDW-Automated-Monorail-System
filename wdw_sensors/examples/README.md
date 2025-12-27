# Examples

This directory contains examples for using the WDW Monorail Sensors Library in various languages.

## Python
- **Basic Usage**: `dht22_example.py`, `mpu6050_example.py`
- **CLI Usage**: `cli_example.py`
- **Advanced Usage**: `advanced_example.py`
- **Visualization**: `visualization_example.py`
- **MQTT**: `mqtt_example.py`
- **API**: `api_example.py`

## Java
- **Basic Usage**: `java_example.java`

## Ruby
- **Basic Usage**: `ruby_example.rb`

## C
- **Basic Usage**: `c_example.c`

## C++
- **Basic Usage**: `cpp_example.cpp`

## Running Examples

### Python
```bash
python dht22_example.py
```

### Java
```bash
javac -cp .:wdw-sensors.jar java_example.java
java -cp .:wdw-sensors.jar JavaExample
```

### Ruby
```bash
ruby ruby_example.rb
```

### C
```bash
gcc -o c_example c_example.c -lwdw_sensors -lpigpio
./c_example
```

### C++
```bash
g++ -o cpp_example cpp_example.cpp -lwdw_sensors -lpigpio
./cpp_example
```

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
