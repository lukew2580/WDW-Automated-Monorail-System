# WDW Monorail Sensor Framework

## 🚝 Comprehensive Sensor System for WDW Monorail Operations

A complete sensor framework for the Walt Disney World Monorail System, providing realistic sensor coverage across all operational lines, stations, and maintenance facilities.

## 📦 Features

- **System-Wide Coverage**: Sensors for monorails, stations, TTC, and maintenance
- **Realistic Sensor Types**: LiDAR, ultrasonic, IR, and proximity sensors
- **CAD Integration Ready**: JSON-based data format for easy import
- **Override Scenarios**: Safety protocol testing framework
- **Comprehensive Documentation**: Complete system specifications

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/wdw-monorail-sensors.git
cd wdw-monorail-sensors

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from sensor_framework import MonorailSensorSystem

# Initialize the system
system = MonorailSensorSystem()

# Load default configuration
system.load_default_config()

# Generate sensor data
sensor_data = system.generate_sensor_data()

# Save for CAD integration
system.save_to_json('monorail_sensors.json')
```

## 📚 Documentation

### System Architecture

```
WDW-Monorail-Sensors/
├── sensor_framework.py          # Main framework
├── system_wide_sensor_framework.py # Complete system implementation
├── sensor_specifications.json   # Sensor technical specs
├── README.md                    # This file
├── LICENSE                      # License information
├── requirements.txt             # Dependencies
└── docs/                        # Additional documentation
```

### Sensor Types

| Sensor ID | Type | Location | Purpose |
|-----------|------|---------|---------|
| A | ToF LiDAR + Ultrasonic | Front nose | Collision avoidance |
| B | Ultrasonic + IR | Rear end | Rear obstacle detection |
| C1/C2 | LiDAR arrays | Side panels | Side collision detection |
| D | IR proximity | Undercarriage | Ground clearance monitoring |
| E | Ultrasonic | Door areas | Passenger safety |
| F | LiDAR | Top | Overhead clearance |

### Station Sensors

- **TTC**: 9 sensors (3×3 grid) for comprehensive coverage
- **Epcot Station**: 3 sensors for platform monitoring
- **Resort Hotels**: 1-2 sensors per station for arrival/departure
- **Maintenance Barn**: 5 sensors for parking and maintenance operations

## 🔧 Configuration

### Customizing Sensor Layout

```python
# Custom sensor configuration
config = {
    "monorails": 9,
    "resort_stations": 3,
    "ttc_sensors": 9,
    "epcot_sensors": 3,
    "barn_sensors": 5,
    "maintenance_sensors": 4
}

system = MonorailSensorSystem(config)
system.generate_sensor_data()
```

### Sensor Specifications

Edit `sensor_specifications.json` to modify sensor parameters:

```json
{
  "A": {
    "name": "Front Proximity Detection",
    "type": "ToF LiDAR + Ultrasonic",
    "range": "0.1m - 5m",
    "frequency": "40Hz",
    "location": "Front nose of monorail",
    "purpose": "Collision avoidance, obstacle detection"
  }
}
```

## 📊 Data Format

### JSON Output Structure

```json
{
  "monorails": {
    "M1": {
      "position": [0, 0, 0],
      "sensors": {
        "A": {"type": "ToF LiDAR", "status": "active", "data": {...}},
        "B": {"type": "Ultrasonic", "status": "active", "data": {...}}
      }
    }
  },
  "stations": {
    "TTC": {
      "sensors": [
        {"id": "TTC_1", "type": "LiDAR", "position": [10, 5, 2], "coverage": "platform"},
        ...
      ]
    }
  }
}
```

## 🧪 Testing

### Running Tests

```bash
# Run unit tests
python -m unittest discover tests/

# Run integration tests
python tests/integration_test.py
```

### Test Coverage

- ✅ Sensor initialization
- ✅ Data generation
- ✅ JSON serialization
- ✅ CAD integration format
- ✅ Override scenarios

## 🎯 CAD Integration

### Importing into CAD Systems

```python
import json

# Load sensor data
with open('monorail_sensors.json', 'r') as f:
    sensor_data = json.load(f)

# Process for your CAD system
for monorail_id, monorail_data in sensor_data['monorails'].items():
    position = monorail_data['position']
    sensors = monorail_data['sensors']
    
    # Create monorail in CAD at position
    # Add sensors at specified locations
    # Configure sensor properties
```

### Coordinate System

- **Units**: Meters
- **Origin**: TTC center point
- **X-axis**: East direction
- **Y-axis**: North direction
- **Z-axis**: Elevation (meters above ground)

## 📋 Requirements

```
Python 3.8+
No external dependencies required
```

## 🔄 Version History

- **v1.0.0**: Initial release - Complete sensor framework
- **v1.0.1**: Added comprehensive documentation
- **v1.0.2**: Enhanced CAD integration support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📬 Contact

For questions or support:
- **Email**: monorail-sensors@wdw.com
- **Documentation**: [Complete Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/wdw-monorail-sensors/issues)

## 🏗️ Roadmap

- **v1.1.0**: Real-time sensor simulation
- **v1.2.0**: CAD plugin integration
- **v2.0.0**: IoT sensor connectivity

---

© 2025 WDW Monorail Systems. All rights reserved.

