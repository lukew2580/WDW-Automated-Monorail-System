# WDW Automated Monorail System

🚂 **Fully automated Disney Monorail playset control system** using Raspberry Pi and Bluetooth

## Overview

Transform your Disney Monorail playset into a professional automated system with:

- ✅ **Bluetooth Control** - Wireless communication with Raspberry Pi
- ✅ **Station Management** - Automated stops, boarding, and departures
- ✅ **Speed Control** - Dynamic speed adjustment
- ✅ **Web Dashboard** - Real-time monitoring and control
- ✅ **REST API** - Programmatic control & automation
- ✅ **JARVIS Integration** - Voice commands ("Take me to Magic Kingdom")

## Hardware Requirements

- **Raspberry Pi 4** (4GB+ RAM recommended)
- **Disney Monorail Playset** (motorized)
- **Bluetooth Module** (HC-05 or compatible)
- **Relay Module** (for motor control)
- **Power Supply** (appropriate for your motor)
- **Jumper Wires & USB Cable**

## Software Stack

- **Python 3.9+**
- **FastAPI** - REST API server
- **Bleak** - Bluetooth Low Energy (BLE) communication
- **AsyncIO** - Async runtime

## Installation

### 1. On Raspberry Pi

```bash
git clone https://github.com/lukew2580/WDW-Automated-Monorail-System.git
cd WDW-Automated-Monorail-System
pip install -r requirements.txt
```

### 2. Wire Raspberry Pi to Motor/Monorail

```
Raspberry Pi GPIO Pins:
  - GPIO 17: Motor Forward
  - GPIO 18: Motor Backward
  - GPIO 27: Speed PWM (pulse width modulation)
  - GND: Ground
  - 5V: Power
```

### 3. Pair Bluetooth Module

```bash
bluetoothctl
scan on
pair <HC-05_MAC_ADDRESS>
trust <HC-05_MAC_ADDRESS>
```

## Usage

### Start the API Server

```bash
python api_server.py
```

Server runs at `http://127.0.0.1:8002`

### Test with Dashboard

Open `dashboard.html` in a browser

### Control via API

**Start Monorail**
```bash
curl -X POST http://127.0.0.1:8002/monorail/start
```

**Go to Station**
```bash
curl -X POST http://127.0.0.1:8002/monorail/go-to-station/epcot
```

**Set Speed**
```bash
curl -X POST http://127.0.0.1:8002/monorail/speed/50
```

**Get Status**
```bash
curl http://127.0.0.1:8002/monorail/status
```

## Files

| File | Purpose |
|------|---------|
| `monorail_controller.py` | Bluetooth/GPIO motor control |
| `station_system.py` | Station logic & automation |
| `api_server.py` | REST API server |
| `dashboard.html` | Web control interface |
| `requirements.txt` | Python dependencies |

## Features

### ✅ Implemented

- [x] API server & REST endpoints
- [x] Web dashboard
- [x] Station management system
- [x] Speed control
- [x] Route management

### 🚧 In Progress

- [ ] Hardware integration (GPIO/BLE)
- [ ] Raspberry Pi deployment
- [ ] Real monorail testing
- [ ] JARVIS voice integration

### 📋 Planned

- [ ] Web app (React)
- [ ] Mobile app (iOS/Android)
- [ ] Automation/scheduling
- [ ] Multi-monorail support
- [ ] Real-time tracking

## Testing

### Run Station System Simulation

```bash
python station_system.py
```

### Run API Tests

```bash
python test_api.py
```

## JARVIS Integration

Control your monorail via voice:

```
"Jarvis, take me to Magic Kingdom"
"Jarvis, set monorail speed to 75%"
"Jarvis, stop at the next station"
```

## Documentation

- [Setup Guide](docs/SETUP.md)
- [API Reference](docs/API.md)
- [Hardware Wiring](docs/WIRING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## License

MIT License - See LICENSE file

## Author

Luke Williams (@lukew2580)

---

**Status**: 🚧 In Development  
**Last Updated**: 2025-12-15  
**Next Milestone**: Hardware integration & Raspberry Pi deployment

