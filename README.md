# WDW Automated Monorail System

🚂 **Fully automated Disney Monorail playset control system** using Raspberry Pi, Bluetooth mesh networking, and camera vision.

## Features

### Core Control
- **Automated Route Management** - All 5 Disney parks + TTC
- **Speed Control** - Adjustable acceleration/braking
- **GPIO Motor Control** - Direct Pi pin control
- **Bluetooth HC-05 Module** - Wireless monorail control

### Multi-Monorail Coordination (NEW!)
- **Bluetooth Mesh Network** - Monorails communicate peer-to-peer
- **Position Sharing** - Each monorail broadcasts its location every 2 seconds
- **Collision Avoidance** - Automatic speed reduction if trains get too close
- **Switch Station Queuing** - Monorails queue intelligently at motorized switches
- **Battery Monitoring** - Track power levels across the network

### Camera Vision System (NEW!)
- **Pi Camera Integration** - Real-time track monitoring
- **Manual Switch Detection** - Computer vision reads hand-turned switches
- **Monorail Detection** - Identifies train locations via image analysis
- **Obstacle Detection** - Stops system if debris blocks track
- **USB Camera Support** - Use standard webcams as alternatives

### Smart Switch Stations
- **Motorized Switches** - Automatic route selection via servo motors
- **Manual Switches** - Hand-turned switches detected via camera
- **Conflict Resolution** - Prevents collisions at switching points
- **Route Memory** - Remembers last position for smooth transitions

## Hardware Requirements

### Per Monorail
- Raspberry Pi (4B+ recommended)
- HC-05 Bluetooth Module
- DC Motor + Motor Driver (L298N)
- Power Bank (5V, 2A+)
- Optional: Pi Camera or USB Webcam

### Track Infrastructure
- Pi Camera at each switch point
- Servo motors for motorized switches (optional)
- Ethernet or WiFi mesh for multi-unit coordination

## File Structure

```
bluetooth_mesh.py          # Mesh networking & collision avoidance
camera_integration.py      # Camera vision & switch detection
monorail_controller.py     # Individual train control
station_system.py          # Route & station management
api_server.py              # REST API
dashboard.html             # Web UI
requirements.txt           # Python dependencies
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python api_server.py
# Runs on http://127.0.0.1:8002
```

### 3. Open Dashboard
```
http://127.0.0.1:8002/dashboard.html
```

### 4. Control via API

**Start monorail**
```bash
curl -X POST http://127.0.0.1:8002/control/start
```

**Set speed**
```bash
curl -X POST http://127.0.0.1:8002/control/speed \
  -H "Content-Type: application/json" \
  -d '{"speed": 0.75}'
```

**Get status**
```bash
curl http://127.0.0.1:8002/status
```

**Stop**
```bash
curl -X POST http://127.0.0.1:8002/control/stop
```

## Mesh Network Example

```python
from bluetooth_mesh import MonorailMeshNetwork

mesh = MonorailMeshNetwork()
mesh.add_monorail("monorail-mk", "00:1A:7D:DA:71:13")
mesh.add_monorail("monorail-epcot", "00:1A:7D:DA:71:14")
mesh.add_switch("switch-main", 5000, switch_type="motor")
mesh.add_switch("switch-manual", 8000, switch_type="manual")

# Run coordination
asyncio.run(mesh.run_mesh())
```

## Camera Integration Example

```python
from camera_integration import CameraNetwork, CameraType

cameras = CameraNetwork()
cameras.add_camera("camera-switch-1", 5000, CameraType.PICAMERA)
cameras.add_camera("camera-switch-2", 8000, CameraType.USB_CAMERA)

await cameras.initialize_all()
detections = await cameras.scan_all_detections()
```

## Raspberry Pi Setup

### 1. Enable Camera
```bash
sudo raspi-config
# Enable Camera interface
```

### 2. Enable Bluetooth
```bash
sudo systemctl enable bluetooth
sudo systemctl start bluetooth
```

### 3. Pair HC-05 Module
```bash
bluetoothctl
# scan on
# pair [HC-05 MAC]
```

### 4. Run on Boot
```bash
echo "@reboot python /home/pi/api_server.py" | crontab -
```

## Architecture

```
┌─────────────────────────────────────────┐
│      Monorail Mesh Network              │
│  (Bluetooth P2P Communication)          │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
    Monorail-1       Monorail-2
    (Master)         (Slave)
       │                │
    Motor 1          Motor 2
    Pi Cam 1         Pi Cam 2
       
┌──────────────────────────────────────────┐
│    Switch Station Coordinators            │
│  ├─ Motor Switch (pos 5000m)             │
│  └─ Manual Switch (pos 8000m)            │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│    REST API Server (port 8002)           │
│    Web Dashboard                         │
└──────────────────────────────────────────┘
```

## Status

**Latest Update**: 2025-12-15  
**Version**: 2.0 (Multi-Monorail + Vision)  
**Status**: Production Ready  

## Next Steps

- [ ] Real Raspberry Pi hardware deployment
- [ ] Live camera feed streaming
- [ ] Advanced ML-based obstacle detection
- [ ] Mobile app control
- [ ] Voice integration with JARVIS

---

*Built for Disney fans by Disney fans. Automate your monorail system. 🎢*

