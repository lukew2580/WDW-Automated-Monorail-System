# Raspberry Pi Backend Architecture
## WDW Automated Monorail System

## Overview
This document describes the software architecture and implementation strategy for the Raspberry Pi backend that manages the hybrid WiFi/Bluetooth mesh network for the WDW Automated Monorail System.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                          │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐  │
│  │  Web Dashboard │  │  Mobile App    │  │  Voice API    │  │
│  │   (Node.js)    │  │  (React Native)│  │  (Optional)   │  │
│  └────────┬───────┘  └────────┬───────┘  └───────┬───────┘  │
│           │                    │                   │          │
└───────────┼────────────────────┼───────────────────┼──────────┘
            │                    │                   │
┌───────────┼────────────────────┼───────────────────┼──────────┐
│           ▼                    ▼                   ▼          │
│    ┌──────────────────────────────────────────────────┐      │
│    │         API Gateway Layer (Express.js)          │      │
│    │  REST API | WebSocket | MQTT Bridge             │      │
│    └──────────────────────────────────────────────────┘      │
│                           │                                  │
│    ┌──────────────────────┴──────────────────────────┐       │
│    │                                                  │       │
│    ▼                                                  ▼       │
│ ┌────────────────────┐                  ┌─────────────────┐ │
│ │   MQTT Broker      │                  │ BLE Controller  │ │
│ │   (Mosquitto)      │                  │  (Bluetooth lib)│ │
│ │                    │                  │                 │ │
│ │  - Device registry │                  │ - BLE scanning  │ │
│ │  - Message routing │                  │ - Pairing logic │ │
│ │  - Subscriptions   │                  │ - Data collection│ │
│ └────────────────────┘                  └─────────────────┘ │
│           │                                       │          │
└───────────┼───────────────────────────────────────┼──────────┘
            │                                       │
┌───────────┼───────────────────────────────────────┼──────────┐
│           ▼                                       ▼          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │        SERVICE LAYER (Python/Node.js)              │    │
│  │  ┌──────────────────┐  ┌──────────────────┐       │    │
│  │  │ Sensor Service   │  │ Monorail Service │       │    │
│  │  │  - Aggregation   │  │  - Tracking      │       │    │
│  │  │  - Validation    │  │  - Coordination  │       │    │
│  │  │  - Filtering     │  │  - Commands      │       │    │
│  │  └──────────────────┘  └──────────────────┘       │    │
│  │  ┌──────────────────┐  ┌──────────────────┐       │    │
│  │  │ Audio Service    │  │ Automation       │       │    │
│  │  │  - Sync logic    │  │ Service          │       │    │
│  │  │  - Playback      │  │  - Rules engine  │       │    │
│  │  │  - Messaging     │  │  - Triggers      │       │    │
│  │  └──────────────────┘  └──────────────────┘       │    │
│  │  ┌──────────────────┐  ┌──────────────────┐       │    │
│  │  │ Analytics Service│  │ Config Service   │       │    │
│  │  │  - Data logging  │  │  - Scenario mgmt │       │    │
│  │  │  - Reporting     │  │  - Settings      │       │    │
│  │  └──────────────────┘  └──────────────────┘       │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            │                                       │
┌───────────┼───────────────────────────────────────┼──────────┐
│           ▼                                       ▼          │
│  ┌───────────────────┐  ┌─────────────────────────────┐    │
│  │   Data Layer      │  │  Device Communication       │    │
│  │                   │  │                             │    │
│  │ ┌───────────────┐ │  │ ┌───────────────────────┐   │    │
│  │ │  SQLite/      │ │  │ │ WiFi Device Driver    │   │    │
│  │ │  PostgreSQL   │ │  │ │ (REST/MQTT)           │   │    │
│  │ │                 │ │  │ ├─ Track Sensors      │   │    │
│  │ │ - Device data │ │  │ │ ├─ Motion Sensors    │   │    │
│  │ │ - Scenarios   │ │  │ │ ├─ Audio Relays      │   │    │
│  │ │ - Logs        │ │  │ │ └─ Mesh Nodes        │   │    │
│  │ └───────────────┘ │  │ │                       │   │    │
│  │ ┌───────────────┐ │  │ └───────────────────────┘   │    │
│  │ │  InfluxDB     │ │  │ ┌───────────────────────┐   │    │
│  │ │  (Time series)│ │  │ │ BLE Device Driver     │   │    │
│  │ │                 │ │  │ (Bluez/PyBluez)       │   │    │
│  │ │ - Metrics     │ │  │ ├─ Monorail Units      │   │    │
│  │ │ - Events      │ │  │ ├─ BLE Repeaters       │   │    │
│  │ │ - History     │ │  │ └─ Sensors             │   │    │
│  │ └───────────────┘ │  │ └───────────────────────┘   │    │
│  └───────────────────┘  └─────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            │                                       │
┌───────────┼───────────────────────────────────────┼──────────┐
│           ▼                                       ▼          │
│  ┌────────────────────────────────────────────────────┐     │
│  │           DEVICE LAYER (Hardware)                 │     │
│  │  ┌──────────────┐              ┌───────────────┐  │     │
│  │  │  WiFi        │              │  Bluetooth 5.0│  │     │
│  │  │  Adapter     │              │  Module       │  │     │
│  │  │  (2.4/5GHz)  │              │  (Built-in)   │  │     │
│  │  └──────────────┘              └───────────────┘  │     │
│  │  ┌──────────────┐              ┌───────────────┐  │     │
│  │  │  Ethernet    │              │  GPIO Pins    │  │     │
│  │  │  (PoE RX)    │              │  (Expansion)  │  │     │
│  │  └──────────────┘              └───────────────┘  │     │
│  └────────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Core Services

### 1. **Sensor Service** (Python)
Manages all WiFi-connected track sensors.

```python
class SensorService:
    - subscribe_to_mqtt_topics()     # Listen to sensor data
    - validate_sensor_data()          # Check data integrity
    - aggregate_proximity_readings()  # Process position data
    - update_environmental_data()     # Store environment metrics
    - trigger_automation_rules()      # Execute based on conditions
    - get_sensor_status()             # Report health
```

**Responsibilities**:
- Collect data from WiFi sensors (proximity, motion, environment)
- Validate and filter noisy data
- Aggregate readings to determine monorail position
- Trigger automation rules when conditions are met
- Store sensor data in InfluxDB for time-series analysis

---

### 2. **Monorail Service** (Python)
Manages BLE monorail units and tracking.

```python
class MonorailService:
    - scan_ble_devices()              # Discover monorails
    - establish_connection()           # BLE pairing
    - track_position()                 # Real-time location
    - send_command()                  # Control monorail
    - get_telemetry()                 # Speed, status, power
    - coordinate_multiple()           # Multi-monorail logic
```

**Responsibilities**:
- Discover and pair with BLE monorail units
- Track monorail position using BLE signal strength and position sensors
- Receive telemetry data (speed, power, status)
- Send commands to monorails (start, stop, sync)
- Coordinate movement across multiple monorails
- Manage BLE mesh repeaters

---

### 3. **Audio Service** (Node.js)
Synchronizes audio playback across the speaker mesh.

```javascript
class AudioService {
    - playSound(location, soundFile)   // Play at specific location
    - syncPlayback()                   // Synchronize all speakers
    - manageSpeakerZones()             // Zone-based playback
    - routeAudioViaWiFi()              // Sonos/Shelly routing
    - routeAudioViaBLE()               // BLE mesh speakers
    - getPlaybackStatus()              // Current state
}
```

**Responsibilities**:
- Manage WiFi speaker network (Sonos, Shelly, etc.)
- Manage BLE mesh speaker network (IKEA, Philips Hue, etc.)
- Synchronize audio across zones
- Handle audio routing based on monorail location
- Support dynamic playlist creation
- Handle audio buffer and latency compensation

---

### 4. **Automation Service** (Python)
Executes automation rules and scenarios.

```python
class AutomationService:
    - register_rule()                 # Add new automation
    - evaluate_conditions()           # Check if rule triggers
    - execute_action()                # Run action (sound, light, etc.)
    - create_scenario()               # Multi-step show program
    - play_scenario()                 # Execute show sequence
    - get_active_automations()        # List enabled rules
```

**Responsibilities**:
- Define and store automation rules (if X, then Y)
- Evaluate conditions in real-time based on sensor data
- Trigger actions (audio, lighting, monorail commands)
- Support scenario/show programming (timed sequences)
- Handle rule priority and conflicts
- Provide logging and debugging

---

### 5. **Analytics Service** (Node.js + InfluxDB/Grafana)
Collects and visualizes system data.

```javascript
class AnalyticsService {
    - logEvent()                      // Record events
    - queryMetrics()                  // Retrieve historical data
    - generateReport()                // Create performance reports
    - createDashboard()               // Grafana integration
    - exportData()                    // CSV/JSON export
}
```

**Responsibilities**:
- Store time-series data in InfluxDB
- Generate Grafana dashboards for visualization
- Track system performance and health
- Export data for analysis
- Provide historical playback capability

---

## Technology Stack

### Backend Runtime
- **Raspberry Pi OS** (Debian-based)
- **Python 3.9+** (Services)
- **Node.js 18+** (API, Dashboard)
- **Systemd** (Service management)

### Core Libraries

#### Python
```
paho-mqtt==1.6.1          # MQTT client
bleak==0.20.0             # BLE scanning/control
aiohttp==3.8.0            # Async HTTP
influxdb-client==1.18.0   # InfluxDB
sqlalchemy==2.0.0         # Database ORM
python-dotenv==0.21.0     # Environment config
```

#### Node.js
```
express==4.18.0           # Web framework
socket.io==4.5.0          # Real-time WebSocket
mqtt==4.2.0               # MQTT client
axios==1.3.0              # HTTP requests
influx==5.9.0             # InfluxDB client
```

### Database
- **SQLite** (Local, small deployments)
- **PostgreSQL** (Intermediate/Advanced)
- **InfluxDB** (Time-series metrics)

### Message Queue
- **Mosquitto** (MQTT broker)

### Monitoring & Visualization
- **Grafana** (Dashboard visualization)
- **InfluxDB** (Time-series data)

## Data Flow

### Sensor Data Flow
```
WiFi Sensor → MQTT Topic → Mosquitto → Python Service
  ↓
Validation & Aggregation
  ↓
Database (SQLite/PostgreSQL)
  ↓
InfluxDB (Metrics)
  ↓
Dashboard / Rules Engine
```

### Monorail Tracking Flow
```
BLE Monorail ←→ Raspberry Pi (BLE Scanner)
     ↓
Position Calculation (Trilateration)
     ↓
Service Layer
     ↓
Audio Service (Trigger sounds)
     ↓
Automation Engine (Execute rules)
```

### Audio Command Flow
```
Web Dashboard / Mobile App
     ↓
REST API / WebSocket
     ↓
Audio Service
     ↓
WiFi Speakers (Sonos/Shelly) → Audio Output
BLE Mesh Speakers (IKEA/Philips) → Audio Output
```

## Configuration Structure

```
/etc/wdw-monorail/
├── config.yaml              # Main configuration
├── devices.json             # Device registry
├── sensors/
│   ├── proximity.yaml       # Proximity sensor config
│   ├── environmental.yaml   # Environmental sensor config
│   └── motion.yaml          # Motion sensor config
├── monorails/
│   ├── resort-line.yaml     # Resort monorail config
│   ├── express-line.yaml    # Express monorail config
│   └── epcot-line.yaml      # Epcot monorail config
├── audio/
│   ├── speakers.yaml        # Speaker configuration
│   ├── zones.yaml           # Audio zone mapping
│   └── sounds/              # Audio files directory
├── automation/
│   ├── rules.yaml           # Automation rules
│   └── scenarios/           # Show/scenario definitions
└── logging/
    └── log.conf             # Logging configuration
```

## API Endpoints

### REST API (Express.js)

**Sensor Management**
```
GET  /api/sensors              # List all sensors
GET  /api/sensors/:id          # Get sensor details
POST /api/sensors              # Register new sensor
PUT  /api/sensors/:id          # Update sensor config
```

**Monorail Management**
```
GET  /api/monorails            # List all monorails
GET  /api/monorails/:id        # Get monorail status
POST /api/monorails/:id/cmd    # Send command
GET  /api/monorails/:id/track  # Get position tracking
```

**Audio Control**
```
POST /api/audio/play           # Play sound at location
POST /api/audio/stop           # Stop playback
POST /api/audio/sync           # Synchronize speakers
GET  /api/audio/status         # Get playback status
```

**Automation**
```
GET  /api/automation/rules     # List rules
POST /api/automation/rules     # Create rule
PUT  /api/automation/rules/:id # Update rule
DELETE /api/automation/rules/:id # Delete rule
```

**Analytics**
```
GET  /api/analytics/metrics    # Retrieve metrics
GET  /api/analytics/export     # Export data
GET  /api/analytics/dashboard  # Dashboard data
```

## Installation & Deployment

### Quick Start
```bash
# Clone repository
git clone https://github.com/lukew2580/WDW-Automated-Monorail-System.git
cd WDW-Automated-Monorail-System

# Install dependencies
./scripts/install-deps.sh

# Configure system
cp config.example.yaml config.yaml
nano config.yaml  # Edit configuration

# Start services
systemctl start wdw-monorail-backend
systemctl start wdw-monorail-api
systemctl start mosquitto

# Access dashboard
# Open browser: http://raspberry-pi-ip:3000
```

### Docker Support (Advanced)
```bash
docker-compose up -d
```

## Performance Considerations

- **BLE Scanning**: 2-5 second update intervals
- **Sensor Polling**: 1 second intervals (adjustable)
- **Audio Sync Latency**: <100ms across speakers
- **Database Query Time**: <500ms for analytics queries
- **Memory Usage**: ~200-400MB on Raspberry Pi 4 (8GB)
- **CPU Load**: 15-25% under normal operation

## Security

- **MQTT Auth**: Username/password authentication
- **API Auth**: JWT tokens for web dashboard
- **BLE Pairing**: Secure pairing with PIN verification
- **Network Isolation**: Guest network for devices
- **Data Encryption**: Optional TLS for sensitive communications

## Future Enhancements

- Kubernetes support for multi-Pi deployments
- WebRTC for video monitoring
- Machine learning for predictive automation
- Voice command integration (Alexa, Google Home)
- 5G/LTE failover support
- Distributed database replication


