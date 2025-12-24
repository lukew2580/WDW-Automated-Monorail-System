# Hybrid Mesh Network Vision
## WDW Automated Monorail System - Comprehensive System Design

---

## Executive Summary

The WDW Automated Monorail System represents a breakthrough in home automation and entertainment technology by combining three decades of Disney monorail experience with modern IoT technology. The hybrid WiFi/Bluetooth mesh network architecture provides a scalable, modular platform that grows with user needs.

**Core Principle**: *Start simple, grow complex. Build once, expand forever.*

---

## System Architecture Overview

### Three-Layer Network Stack

```
┌─────────────────────────────────────────────────┐
│         AUDIO DISTRIBUTION LAYER                │
│      (WiFi & BLE Hybrid Mesh Network)          │
│  Sonos • Shelly • IKEA DIRIGERA • Philips Hue │
└─────────────────────────────────────────────────┘
           ↓         ↓         ↓         ↓
┌─────────────────────────────────────────────────┐
│      CENTRAL COORDINATION LAYER                 │
│     (Raspberry Pi Backend Services)             │
│  Sensor Service • Monorail Service              │
│  Audio Service • Automation Engine              │
└─────────────────────────────────────────────────┘
           ↓         ↓         ↓         ↓
┌─────────────────────────────────────────────────┐
│        NETWORK & TRACKING LAYER                 │
│  ┌──────────────────┐   ┌────────────────────┐ │
│  │  WiFi Track      │   │  BLE Monorails     │ │
│  │  Sensors         │   │  & Repeaters       │ │
│  │  (Position, Env) │   │  (Real-time Track) │ │
│  └──────────────────┘   └────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Why This Architecture?

#### **WiFi Track Sensors** (Stationary)
✓ Wired power available on track  
✓ Stable, long-range connectivity (100m+)  
✓ Can use PoE to reduce wiring  
✓ More frequent, reliable updates  
✓ Environmental monitoring capability  

#### **BLE Monorail Units** (Mobile)
✓ Battery-powered, lightweight  
✓ Real-time position tracking  
✓ Direct communication with track sensors  
✓ Lower power consumption  
✓ Mesh-capable for extended range  

#### **Hybrid Audio Mesh** (Flexible)
✓ WiFi speakers for stable playback  
✓ BLE mesh speakers for remote zones  
✓ Automatic fallback routing  
✓ Zone-based audio distribution  
✓ Synchronized across all devices  

---

## Configuration Tiers

### Tier 1: Basic Setup ($400-500)
**For the hobbyist starting out**

```
Components:
  • 1x Raspberry Pi 4 (4GB)
  • 3x Tuya WiFi Ultrasonic Sensors
  • 3x Tile Slim BLE Beacons
  • 2x Shelly WiFi Relays + Passive Speakers
  • Standard WiFi Router

Features:
  ✓ Basic monorail tracking
  ✓ Simple audio triggers
  ✓ Manual control dashboard
  ✗ No mesh network
  ✗ Limited automation
```

### Tier 2: Intermediate Setup ($800-1200)
**For the enthusiast wanting more**

```
Components:
  • 1x Raspberry Pi 4 (8GB)
  • 5x Shelly Plus H&T Sensors
  • 3x Adafruit Bluefruit BLE modules
  • 2x BLE Mesh Repeaters
  • 3x Sonos One Speakers
  • 2x IKEA DIRIGERA Hubs + Speakers
  • WiFi Mesh Network (2-3 nodes)

Features:
  ✓ Full mesh networking
  ✓ Advanced automation
  ✓ Synchronized audio zones
  ✓ Environmental monitoring
  ✓ Web dashboard & mobile app
  ✓ InfluxDB analytics
```

### Tier 3: Advanced Setup ($1500-2500)
**For the professional installation**

```
Components:
  • Master + 2x Secondary Raspberry Pi 4 (8GB)
  • 8-10x Comprehensive Sensor Array
  • 5x Nordic nRF52840 BLE Modules
  • 5x Professional BLE Mesh Repeaters
  • 5-6x Sonos Arc/Playbar Speakers
  • 3-4x Philips Hue Play Speakers
  • 2x Professional PoE Audio Amplifiers
  • Professional WiFi Mesh (Ubiquiti UniFi)

Features:
  ✓ All Tier 2 features
  ✓ Redundant backend with failover
  ✓ Professional audio quality
  ✓ Voice integration (Alexa/Google)
  ✓ Video monitoring
  ✓ Advanced analytics
  ✓ Multi-user concurrent control
  ✓ Show programming
```

---

## Data Flow Architecture

### Sensor Data Pipeline
```
Physical Sensor (WiFi)
    ↓
MQTT Topic (Mosquitto)
    ↓
Python Sensor Service (Validation, Filtering)
    ↓
SQLite/PostgreSQL Database
    ↓
InfluxDB (Time-series Metrics)
    ↓
Grafana Dashboards / REST API / WebSocket
    ↓
Web Dashboard / Mobile App / Automation Engine
```

### Monorail Tracking Pipeline
```
BLE Monorail Unit (Broadcasting)
    ↓
Raspberry Pi BLE Scanner
    ↓
Position Calculation (Trilateration)
    ↓
Python Monorail Service
    ↓
Real-time Database Updates
    ↓
Audio Service (Sound Triggers)
    ↓
Automation Engine (Rule Execution)
```

### Audio Distribution Pipeline
```
Central Automation Engine
    ↓
Audio Service (Route Selection)
    ├→ WiFi Speaker Group (Sonos, Shelly)
    └→ BLE Mesh Speaker Group (IKEA, Philips)
    ↓
Zone-Based Playback (Synchronized)
    ↓
Speaker Mesh (Automatic Failover)
    ↓
Audio Output to Destination
```

---

## The Hybrid Mesh Concept

### WiFi Mesh Benefits
- Stable backbone for critical data
- Long-range communication
- Supports stationary infrastructure
- Can bridge to internet/cloud (optional)
- PoE power integration

### BLE Mesh Benefits
- Low power for mobile units
- Real-time responsiveness
- Self-healing topology
- Dense coverage in local areas
- Seamless device discovery

### Hybrid Approach Benefits
- **Reliability**: Dual paths for redundancy
- **Coverage**: WiFi for backbone, BLE for dense areas
- **Flexibility**: Use best protocol for each device
- **Future-proof**: Can extend with additional technologies
- **Cost-effective**: Leverage existing WiFi infrastructure

---

## Key Features by Service

### Sensor Service
```
Responsibilities:
  • Aggregate proximity data
  • Validate environmental readings
  • Detect anomalies
  • Trigger basic rules
  
Output:
  • Position coordinates
  • Environmental state
  • Alert events
```

### Monorail Service
```
Responsibilities:
  • Track BLE device locations
  • Manage monorail commands
  • Coordinate multi-unit movement
  • Collect telemetry
  
Output:
  • Real-time position
  • Speed/acceleration
  • Power status
  • Event stream
```

### Audio Service
```
Responsibilities:
  • Manage speaker networks
  • Synchronize playback
  • Handle zone routing
  • Maintain audio queue
  
Output:
  • Audio to speakers
  • Playback status
  • Event triggers
```

### Automation Engine
```
Responsibilities:
  • Evaluate rules
  • Execute actions
  • Manage scenarios
  • Handle conflicts
  
Output:
  • Command execution
  • Event logging
  • Status reports
```

---

## User Scenarios

### Scenario A: Monorail Entrance Announcement
```
Event: Monorail approaches Resort station
  ↓
Sensor 1 detects proximity
  ↓
Automation rule: "IF monorail near Resort THEN play welcome sound"
  ↓
Audio Service routes sound to Resort speakers
  ↓
Welcome announcement plays synchronized
```

### Scenario B: Dynamic Lighting + Sound
```
Event: Express monorail at high speed
  ↓
Monorail Service calculates speed
  ↓
Automation rule: "IF speed > 50mph THEN fast music + red lighting"
  ↓
Audio Service plays fast-paced track
  ↓
Philips Hue speakers change to red lighting
```

### Scenario C: Complex Show Sequence
```
User: Plays "Nighttime Spectacular" show
  ↓
Scenario Engine reads sequence from config
  ↓
Coordinates timing for:
  - Monorail movements
  - Audio cues (multiple zones)
  - Lighting effects
  - Environmental effects
  ↓
All synchronized within 100ms across network
```

---

## CAD Integration

The system includes detailed CAD models showing:

```
monorail_track_layout.png
├─ TTC (Transportation & Ticket Center)
├─ Resort Line (Inner circle)
├─ Express Line (Outer circle)
└─ Epcot Line (Direct route)

monorail_sensor_network_layout.png
├─ Track Sensors (WiFi circles)
├─ Monorail Units (BLE hexagons)
├─ Speakers (Rectangles)
├─ Mesh Repeaters (Diamonds)
└─ Raspberry Pi Backend (Central square)
```

These models serve as the foundation for:
- Physical component placement
- Cable routing planning
- Zone definition
- Coverage mapping
- Future expansion planning

---

## Network Stack Specifications

### WiFi Layer
- **Standard**: 802.11ac (WiFi 5) or 802.11ax (WiFi 6)
- **Frequency**: 2.4GHz (legacy) and 5GHz (preferred)
- **Range**: 100m+ with mesh nodes
- **Bandwidth**: Sufficient for sensors (~10-50 kbps each)
- **Mesh**: Supports self-healing topology

### Bluetooth Layer
- **Standard**: Bluetooth 5.0+ with Mesh support
- **Frequency**: 2.4GHz
- **Range**: 20-30m base, 100m+ with mesh repeaters
- **Bandwidth**: ~1 Mbps (sufficient for position data)
- **Latency**: <100ms

### MQTT Message Queue
- **Broker**: Mosquitto (open-source)
- **Topics**: Hierarchical structure
  - `sensors/proximity/+/position`
  - `monorails/resort/+/telemetry`
  - `audio/zones/+/command`
  - `automation/events/+`

### REST API
- **Server**: Express.js on Node.js
- **Auth**: JWT tokens
- **Format**: JSON
- **Real-time**: WebSocket (Socket.io)

---

## Technology Selection Rationale

### Python for Services
✓ Excellent async support (asyncio)  
✓ Rich IoT library ecosystem  
✓ Easy prototyping  
✓ Strong BLE support (bleak)  
✓ MQTT client libraries (paho)  

### Node.js for API/Dashboard
✓ Real-time WebSocket capability  
✓ Single-language backend/frontend  
✓ Excellent REST API frameworks  
✓ Fast performance  
✓ Easy deployment on Pi  

### SQLite/PostgreSQL for Data
✓ Proven reliability  
✓ Complex query support  
✓ Transaction safety  
✓ Easy backup/restore  

### InfluxDB for Metrics
✓ Optimized for time-series data  
✓ Efficient compression  
✓ Fast range queries  
✓ Easy integration with Grafana  

---

## Performance Targets

### Latency
- Sensor reading → Dashboard: <2 seconds
- Audio trigger → Speaker output: <500ms
- Monorail position update: <1 second
- API response time: <200ms

### Reliability
- WiFi connectivity: >99.5% uptime
- BLE mesh reliability: >95% message delivery
- Audio sync accuracy: ±100ms across all speakers
- System availability: 99% with automatic recovery

### Scalability
- Support 10+ monorail units
- Handle 50+ sensors simultaneously
- Manage 20+ audio zones
- Process 1000+ automation rules

---

## Future Enhancements

### Short Term (2026)
- Voice command integration
- Video monitoring
- Mobile app
- Show scheduling

### Medium Term (2026-2027)
- Machine learning anomaly detection
- Advanced analytics dashboards
- Multi-site synchronization
- Cloud backup integration

### Long Term (2027+)
- 5G/LTE failover support
- Distributed database replication
- AR visualization
- AI-driven automation

---

## Getting Started

### Choose Your Tier
1. Read `SETUP_SCENARIOS.md` for detailed comparisons
2. Calculate your budget and available space
3. Identify which features matter most

### Follow the Roadmap
1. Complete January tasks (documentation)
2. Progress through February-December phases
3. Check off completed tasks as deliverables are created

### Implementation Order
1. Physical layout planning (use CAD models)
2. Network setup (WiFi/BLE infrastructure)
3. Hardware installation (sensors, speakers)
4. Software deployment (Raspberry Pi backend)
5. Testing and optimization

---

## Support & Documentation

### Reference Documents
- `SENSOR_SPECIFICATIONS.md` - Hardware details
- `SETUP_SCENARIOS.md` - Configuration options
- `RASPBERRY_PI_BACKEND_ARCHITECTURE.md` - Software design
- `ROADMAP_2026.md` - Development timeline
- `monorail_sensor_network_layout.png` - Physical diagram

### Community Resources
- GitHub: [lukew2580/WDW-Automated-Monorail-System](https://github.com/lukew2580/WDW-Automated-Monorail-System)
- Documentation: Comprehensive guides and tutorials
- Examples: Configuration files and scenarios
- Support: Community forum and issue tracking

---

## Conclusion

The WDW Automated Monorail System represents a unique convergence of nostalgia, technology, and automation. By thoughtfully designing a hybrid mesh network architecture and providing scalable configuration tiers, we've created a platform that welcomes both enthusiasts starting with a basic setup and professionals building complex installations.

The modular design ensures that users never outgrow the system—it grows with them, from basic monorail tracking to sophisticated multi-zone audio shows with voice control and advanced analytics.

**The future of Disney-themed automation is here. Start building.**


