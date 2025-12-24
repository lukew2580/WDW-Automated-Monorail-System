# WDW Monorail System - Setup Scenarios

This document outlines three different setup configurations based on complexity, budget, and features.

## Scenario 1: Basic Setup
**Target User**: Hobbyist, Small Layout, Budget-Conscious  
**Estimated Budget**: $400-500  
**Setup Time**: 2-3 hours

### Architecture
```
Single Raspberry Pi 4 → WiFi Mesh Network → Track Sensors
                    ↓
              BLE Monorail Units
                    ↓
              2-3 Wireless Speakers
```

### Component Breakdown

#### Track Layer
- **3x Tuya WiFi Ultrasonic Sensors** (proximity detection)
  - Placement: Resort, Express, Epcot track sections
  - Function: Detect monorail position
  - Connection: WiFi direct to Raspberry Pi

#### Monorail Layer
- **3x Tile Slim 2025 BLE Beacons** (one per monorail)
  - Function: Real-time location tracking via BLE
  - Range: 60+ meters (sufficient for home layouts)
  - Battery: 3-year lifespan

#### Audio Distribution
- **2x Shelly Plus i4 WiFi Relays**
  - Function: Trigger audio playback to passive speakers
  - Connection: WiFi to Raspberry Pi
  - Output: 3.5mm jack to powered speakers

- **Passive Speakers** (existing or purchased)
  - Placement: Resort area, Express area
  - Wiring: Direct from Shelly relays

#### Backend
- **Raspberry Pi 4 (4GB RAM)**
  - Built-in WiFi and Bluetooth 5.0
  - Runs central control software
  - Manages sensor data and audio triggers

#### Networking
- **Single WiFi Router** or mesh node as primary hub

### Feature Set
✓ Real-time monorail position tracking  
✓ Basic audio playback at key locations  
✓ Environmental monitoring  
✓ Simple automation rules (e.g., "Play sound when monorail passes Sensor 1")  
✗ Advanced mesh networking  
✗ Multiple synchronized speakers  
✗ Complex audio environments  

### Implementation Steps
1. Set up Raspberry Pi 4 with custom control software
2. Configure WiFi sensors on network
3. Pair BLE beacons with Raspberry Pi
4. Set up Shelly relays and connect to speakers
5. Create automation rules via web dashboard
6. Test and calibrate sensor positions

---

## Scenario 2: Intermediate Setup
**Target User**: Enthusiast, Medium Layout, Balanced Budget  
**Estimated Budget**: $800-1200  
**Setup Time**: 4-6 hours

### Architecture
```
Raspberry Pi 4 (Central Hub)
    ↓
WiFi Mesh Network (2-3 nodes)
    ├→ Track Sensors (WiFi) → Environmental Data
    ├→ Proximity Sensors (WiFi) → Position Detection
    ├→ BLE Mesh Repeaters → Monorail BLE Network
    └→ Wireless Speakers (WiFi + BLE Mesh Hybrid)
```

### Component Breakdown

#### Track Layer
- **5x Shelly Plus H&T Sensors** (Humidity & Temperature with WiFi)
  - Placement: Throughout barn, key track sections
  - Function: Position detection + environmental monitoring
  - Power: PoE for stable operation
  - Connection: WiFi mesh network

- **3x Tuya Smart PIR Motion Sensors**
  - Placement: Barn entrance, key locations
  - Function: Activity detection, automation triggers
  - Connection: WiFi

#### Monorail Layer
- **3x Adafruit Bluefruit LE UART modules**
  - Function: Enhanced BLE communication with monorails
  - Range: 20-30 meters (extended with mesh repeaters)
  - Data: Speed, position, status updates
  - Power: Rechargeable LiPo batteries

- **2x nRF52840-based BLE Mesh Repeaters**
  - Function: Extend BLE range across layout
  - Placement: Strategic high points
  - Connection: BLE mesh protocol

#### Audio Distribution
- **3x Sonos One Speakers** (WiFi Mesh)
  - Placement: Resort, Express, Epcot areas
  - Function: Synchronized playback
  - Features: Individual or grouped playback
  - Connection: WiFi mesh + BLE capable

- **2x IKEA DIRIGERA Hubs with Speakers**
  - Function: Budget-friendly audio + BLE mesh support
  - Placement: Secondary locations
  - Connection: WiFi + Bluetooth Mesh

#### Backend
- **Raspberry Pi 4 (8GB RAM)**
  - Central control and coordination
  - MQTT broker for device communication
  - Web dashboard for management

#### Networking
- **WiFi Mesh System** (TP-Link Deco or similar)
  - 2-3 mesh nodes for full coverage
  - Ensures stable WiFi across entire layout
  - Supports PoE for track sensors

### Feature Set
✓ Real-time position and speed tracking  
✓ Environmental monitoring (temperature, humidity)  
✓ Synchronized audio across multiple speakers  
✓ BLE mesh networking for extended range  
✓ Motion-based automation triggers  
✓ Web dashboard for management  
✓ MQTT-based device communication  
✗ Advanced voice commands  
✗ Complex multi-zone synchronization  
✗ Professional-grade audio mastering  

### Implementation Steps
1. Deploy WiFi mesh network with PoE backbone
2. Install and configure track sensors on mesh
3. Set up MQTT broker on Raspberry Pi
4. Pair BLE monorail units and repeaters
5. Configure Sonos and DIRIGERA speakers
6. Build automation rules and sync settings
7. Create web interface for user control
8. Test full system with all three lines

---

## Scenario 3: Advanced Setup
**Target User**: Professional, Large/Complex Layout, Feature-Rich  
**Estimated Budget**: $1500-2500  
**Setup Time**: 8-12 hours (plus custom development)

### Architecture
```
Distributed Raspberry Pi Backend (Master + 2 Nodes)
    ↓
Redundant WiFi Mesh Network (4+ nodes) + Wired PoE Backbone
    ├→ Advanced Track Sensor Array (WiFi + Wired)
    ├→ Multi-Zone Environmental Monitoring
    ├→ Comprehensive BLE Mesh (5+ Repeaters)
    ├→ Professional Audio System (WiFi + BLE + Wired)
    └→ Voice Integration & AI Coordination
```

### Component Breakdown

#### Track Layer
- **8-10x Shelly Plus H&T Sensors**
  - PoE powered for reliability
  - Placement: Every major track section
  - Function: Precise position, speed, environment data

- **4-5x Eve Outdoor Cam (WiFi)**
  - Placement: Key visual monitoring points
  - Function: Visual feedback, motion detection
  - Data: Video stream, motion events

- **5x Tuya Advanced Proximity Sensors (6m+ range)**
  - Placement: High-precision location points
  - Function: Speed calculation, precise positioning
  - Connection: WiFi mesh

#### Monorail Layer
- **3x Nordic nRF52840 DK Modules** (custom firmware)
  - Function: Advanced BLE 5.0 coordination
  - Range: 240+ meters with antenna
  - Data: Telemetry, status, commands
  - Power: Integrated charging circuit

- **5x BLE Mesh Repeater Nodes**
  - Placement: Distributed around layout
  - Function: True BLE mesh topology
  - Redundancy: Multiple paths for reliability

#### Audio Distribution
- **5-6x Sonos Arc or Playbar** (professional setup)
  - Placement: Primary audio zones (Resort, Express, Epcot, Barn)
  - Function: Professional-grade synchronized playback
  - Features: Spatial audio, group coordination

- **3-4x Philips Hue Play with BLE Mesh**
  - Function: Integrated lighting + audio effects
  - Placement: Secondary zones, accent locations
  - Connection: WiFi + BLE Mesh hybrid

- **2x Professional PoE Audio Amplifiers**
  - Connection: Wired audio backbone
  - Function: Driving passive speaker arrays
  - For: High-fidelity audio in barn environment

- **Passive Speaker Arrays** (4-6 locations)
  - Placement: Distributed around layout
  - Wiring: Direct from amplifiers via PoE audio trunk

#### Backend
- **Master Raspberry Pi 4 (8GB RAM)**
  - Primary control, orchestration
  - MQTT broker, Node.js backend server
  - Web/mobile dashboard

- **2x Secondary Raspberry Pi 4 (4GB RAM)**
  - Local sensor aggregation nodes
  - BLE gateway functions
  - Failover capability

#### Networking
- **Professional WiFi Mesh** (Ubiquiti UniFi)
  - 4-5 access points
  - PoE backbone for track sensors
  - Guest network isolation
  - Advanced monitoring and logging

#### Additional Systems
- **Voice Integration**
  - Optional: Alexa or Google Home bridge
  - Voice commands for manual control
  - Status announcements

- **Data Logging & Analytics**
  - InfluxDB for time-series data
  - Grafana dashboards for visualization
  - Historical analysis of system performance

- **Custom Mobile App**
  - Real-time monorail tracking
  - Manual control interface
  - Scenario/show programming

### Feature Set
✓ Full real-time tracking with sub-second updates  
✓ Comprehensive environmental monitoring  
✓ Professional-grade synchronized audio  
✓ BLE mesh with redundancy and failover  
✓ Advanced automation and AI-driven scenarios  
✓ Voice control integration  
✓ Video monitoring and security  
✓ Web and mobile dashboards  
✓ Data logging, analytics, and reporting  
✓ Multi-user concurrent control  
✓ Show/scenario programming and playback  
✓ Network redundancy and failover  

### Implementation Steps
1. Design and deploy professional PoE network backbone
2. Install comprehensive WiFi mesh with Ubiquiti
3. Deploy master and secondary Raspberry Pi nodes
4. Install complete sensor array across all zones
5. Configure BLE mesh with 5+ repeater nodes
6. Set up professional audio system with zone coordination
7. Deploy InfluxDB and Grafana for analytics
8. Integrate voice control systems
9. Develop custom mobile application
10. Create show programming interface
11. Comprehensive testing and load testing
12. User training and documentation

---

## Scenario Comparison Matrix

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| **Budget** | $400-500 | $800-1200 | $1500-2500 |
| **Setup Time** | 2-3 hrs | 4-6 hrs | 8-12+ hrs |
| **Sensors** | 3-5 | 8-10 | 12-15+ |
| **Speakers** | 2-3 | 5 | 8-10 |
| **Mesh Coverage** | Single point | 2-3 nodes | 4+ nodes |
| **BLE Repeaters** | 0 | 2 | 5+ |
| **Position Accuracy** | ~1 meter | ~0.5 meter | ~10cm |
| **Audio Sync** | Basic | Good | Professional |
| **Redundancy** | None | Limited | Full |
| **Voice Control** | No | Optional | Integrated |
| **Mobile App** | Web only | Web + Mobile | Advanced Mobile |
| **Analytics** | None | Basic | Professional |

---

## Migration Path
Users can start with Basic setup and upgrade to Intermediate or Advanced:
- **Basic → Intermediate**: Add mesh network, more speakers, BLE repeaters
- **Intermediate → Advanced**: Add PoE backbone, secondary Pi nodes, voice integration
- **Modular Design**: All components can be mixed and matched based on needs


