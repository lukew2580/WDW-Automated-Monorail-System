# WDW Monorail System - Audio Trigger Overlay Integration

**Date**: December 23, 2025  
**Status**: Active Development  
**Integration**: Sensor Network + CAD Framework + Audio System

---

## 🎵 Audio Trigger System Overview

This document defines the audio trigger overlay system that integrates with the sensor network layout (39 sensors across 3 monorails) and CAD framework to provide contextual audio cues based on:
- Layout type (Resort, Express, Epcot)
- Seasonal theme (Holiday, Spring, Summer, Fall)
- Character voice (Mickey, Minnie, Cast Member, Automated)

---

## 📊 Audio Trigger Mapping (by Sensor Location)

### MONORAIL SYSTEMS (3 Total)

#### **RESORT MONORAIL (BLE)**
**Sensors**: Resort Sensor 1, 2, 3 (3 sensors)

| **Location** | **Sensor ID** | **Audio Trigger Events** | **Wiring Zone** |
|--------------|---------------|------------------------|-----------------|
| Polynesian Resort Stop | Res-Sen-1 | • Arrival announcement (character-based) • Safety reminder • Seasonal greeting | Zone A1 |
| Grand Floridian Stop | Res-Sen-2 | • Station transition tone • Door open/close alerts • Theme-specific music | Zone A2 |
| Contemporary Stop | Res-Sen-3 | • Platform occupancy alert • Next destination announcement • Off-peak notification | Zone A3 |

**Audio Profile Settings**:
```json
{
  "resort_monorail": {
    "character": "mickey_mouse | minnie_mouse | cast_member | automated",
    "season": "holiday | spring | summer | fall",
    "volume_base": 75,
    "languages": ["english", "spanish", "french"],
    "audio_banks": [
      "arrival_announcements",
      "safety_reminders",
      "seasonal_greetings",
      "door_alerts"
    ]
  }
}
```

**Wiring Configuration**:
- Speaker 1 (WiFi/BLE): Polynesian platform area
- Speaker 2 (WiFi/BLE): Grand Floridian platform area  
- Speaker 3 (WiFi/BLE): Contemporary platform area

---

#### **EXPRESS MONORAIL (BLE)**
**Sensors**: Express Sensor 1, 2, 3 (3 sensors)

| **Location** | **Sensor ID** | **Audio Trigger Events** | **Wiring Zone** |
|--------------|---------------|------------------------|-----------------|
| Magic Kingdom Express Stop | Exp-Sen-1 | • Express-only greeting • Priority passenger announcement • Fast-track boarding | Zone B1 |
| Epcot Express Stop | Exp-Sen-2 | • Destination confirmation • Express service chime • Station-specific theme | Zone B2 |
| TTC Hub (Express) | Exp-Sen-3 | • Transfer notification • Multi-line routing audio • Consolidation alerts | Zone B3 |

**Audio Profile Settings**:
```json
{
  "express_monorail": {
    "character": "mickey_mouse | minnie_mouse | cast_member | automated",
    "season": "holiday | spring | summer | fall",
    "volume_base": 80,
    "priority": "high",
    "audio_banks": [
      "express_announcements",
      "fast_track_alerts",
      "routing_guidance",
      "transfer_notifications"
    ]
  }
}
```

**Wiring Configuration**:
- Speaker 1 (WiFi/BLE): Magic Kingdom express platform
- Speaker 2 (WiFi/BLE): Epcot express platform
- Speaker 3 (WiFi/BLE): TTC hub express area

---

#### **EPCOT MONORAIL (BLE)**
**Sensors**: Epcot Sensor 1, 2 (2 sensors)

| **Location** | **Sensor ID** | **Audio Trigger Events** | **Wiring Zone** |
|--------------|---------------|------------------------|-----------------|
| Epcot Main Stop | Epc-Sen-1 | • Epcot welcome message • World Showcase transition audio • International theme music | Zone C1 |
| Epcot Secondary Stop | Epc-Sen-2 | • Festival announcements (seasonal) • Crowd flow guidance • Queue time alerts | Zone C2 |

**Audio Profile Settings**:
```json
{
  "epcot_monorail": {
    "character": "mickey_mouse | cast_member | automated",
    "season": "holiday | spring_garden | summer | fall_festival",
    "volume_base": 72,
    "audio_banks": [
      "epcot_welcomes",
      "world_showcase_audio",
      "festival_announcements",
      "crowd_guidance"
    ],
    "festival_aware": true
  }
}
```

**Wiring Configuration**:
- Speaker 1 (WiFi/BLE): Epcot main platform
- Speaker 2 (WiFi/BLE): Epcot secondary platform

---

### CENTRAL HUB SYSTEM (TTC - Transportation & Ticket Center)

**Sensors**: TTC-Sen-1 through TTC-Sen-6 (3×3 grid)

| **Grid Location** | **Sensor ID** | **Audio Trigger Events** | **Wiring Zone** |
|------------------|---------------|------------------------|-----------------|
| Grid Position 1-1 | TTC-Sen-1 | • Route selection guidance • Direction announcements | Zone D1 |
| Grid Position 1-2 | TTC-Sen-2 | • Monorail status updates • Boarding queue alerts | Zone D2 |
| Grid Position 1-3 | TTC-Sen-3 | • Wait time announcements • Alternative transport suggestions | Zone D3 |
| Grid Position 2-1 | TTC-Sen-4 | • Welcome to TTC • Resort information • Dining announcements | Zone D4 |
| Grid Position 2-2 | TTC-Sen-5 | • Central coordination hub • Multi-line coordination | Zone D5 |
| Grid Position 2-3 | TTC-Sen-6 | • Emergency broadcast zone • Crowd management audio | Zone D6 |

**Mesh Network Configuration**:
- Mesh Repeater 1: Distributes audio to zones D1-D3
- Mesh Repeater 2: Distributes audio to zones D4-D6
- BLE Mesh: Ensures coverage across entire TTC complex

---

### SUPPORT LOCATIONS

#### **MONORAIL BARN/MAINTENANCE**
**Sensors**: Barn-Sen-1, Barn-Sen-2 (2 sensors)

| **Location** | **Sensor ID** | **Audio Trigger Events** | **Wiring Zone** |
|--------------|---------------|------------------------|-----------------|
| Barn Operations | Barn-Sen-1 | • Vehicle status alerts • Maintenance notifications • Shift change chimes | Zone E1 |
| Consolidation Zone | Barn-Sen-2 | • Consolidation sequence audio • Vehicle ready alerts • Dispatch confirmations | Zone E2 |

**Maintenance Audio Profile**:
```json
{
  "barn_system": {
    "character": "cast_member | automated",
    "volume_base": 85,
    "audio_banks": [
      "status_alerts",
      "maintenance_warnings",
      "dispatch_confirmations",
      "safety_protocols"
    ],
    "priority": "critical"
  }
}
```

---

## 🎭 Character-Based Audio Profiles

### **MICKEY MOUSE Profile**
- Voice: Cheerful, enthusiastic, family-friendly
- Announcements: "Welcome aboard the monorail!"
- Safety: "Please hold on to the handrails!"
- Seasonal: "Happy Holidays from all of us!" (Holiday) / "Spring is in the air!" (Spring)
- Audio Characteristics: Bright, energetic, 3-4 kHz emphasis

### **MINNIE MOUSE Profile**
- Voice: Warm, welcoming, elegant
- Announcements: "Oh boy, welcome aboard!"
- Safety: "For your safety, please remain seated"
- Seasonal: "Welcome to our winter celebration!" (Holiday)
- Audio Characteristics: Warm, friendly, 4-5 kHz emphasis

### **CAST MEMBER Profile**
- Voice: Professional, knowledgeable, helpful
- Announcements: "Thank you for riding the Walt Disney World Monorail"
- Safety: "Please be aware of closing doors"
- Seasonal: Event-specific announcements
- Audio Characteristics: Clear, professional, 2-3 kHz emphasis

### **AUTOMATED Profile**
- Voice: Neutral, efficient, technical
- Announcements: "Monorail boarding complete"
- Safety: Compliance-focused alerts
- Seasonal: Minimal seasonal variation
- Audio Characteristics: Synthetic, 1-2 kHz emphasis

---

## 🌍 Seasonal Audio Variations

### **HOLIDAY SEASON (November - December)**
- Special chimes and jingles
- Holiday-themed character greetings
- Festive background music in stations
- Seasonal safety reminders
- Winter-themed ambient sounds

**Audio Bank**: `holiday_audio_2025.json`

### **SPRING (March - May)**
- Fresh, bright character greetings
- Garden and flower-themed music
- Spring Festival announcements (Epcot)
- Renewal-themed messages
- Lighter, more cheerful tones

**Audio Bank**: `spring_audio_2025.json`

### **SUMMER (June - August)**
- Energetic, upbeat character announcements
- Summer event promotions
- Vacation-mood messaging
- Outdoor adventure themes
- Higher energy audio profiles

**Audio Bank**: `summer_audio_2025.json`

### **FALL (September - October)**
- Harvest and autumn themes
- Epcot Food & Wine Festival audio
- Cozy, welcoming character messages
- Spooky elements (late October)
- Warm, earthy tones

**Audio Bank**: `fall_audio_2025.json`

---

## 📍 CAD Wiring Integration Points

### **Zone Mapping (A1-E2)**

```
RESORT MONORAIL (BLE)          EXPRESS MONORAIL (BLE)         EPCOT MONORAIL (BLE)
├─ Zone A1: Polynesian         ├─ Zone B1: Magic Kingdom      ├─ Zone C1: Epcot Main
├─ Zone A2: Grand Floridian    ├─ Zone B2: Epcot Express      └─ Zone C2: Epcot Secondary
└─ Zone A3: Contemporary       └─ Zone B3: TTC Hub

TTC HUB (WiFi/BLE Mesh)                  BARN/MAINTENANCE (WiFi/BLE)
├─ Zone D1-D3: Platform Grid             ├─ Zone E1: Barn Operations
└─ Zone D4-D6: Central Hub               └─ Zone E2: Consolidation

MESH REPEATER NETWORK:
├─ Mesh Repeater 1 (TTC): Serves D1-D3 + B3 + A2-A3
└─ Mesh Repeater 2 (TTC): Serves D4-D6 + B1-B2 + E1-E2
```

### **Physical Wiring Requirements**

| **Speaker Zone** | **WiFi/BLE Coverage** | **CAD Reference** | **Cable Run** | **Status** |
|-----------------|----------------------|-------------------|---------------|-----------|
| A1 (Polynesian) | BLE Link to Resort-Sen-1 | Platform_A1_Speaker | ~45ft | Planned |
| A2 (Grand Floridian) | BLE Link to Resort-Sen-2 | Platform_A2_Speaker | ~38ft | Planned |
| A3 (Contemporary) | BLE Link to Resort-Sen-3 | Platform_A3_Speaker | ~42ft | Planned |
| B1 (MK Express) | BLE Link to Express-Sen-1 | Platform_B1_Speaker | ~50ft | Planned |
| B2 (Epcot Express) | BLE Link to Express-Sen-2 | Platform_B2_Speaker | ~48ft | Planned |
| B3 (TTC Hub) | WiFi + Mesh Repeater 1 | Hub_B3_Speaker | ~35ft | Planned |
| C1 (Epcot Main) | BLE Link to Epcot-Sen-1 | Platform_C1_Speaker | ~40ft | Planned |
| C2 (Epcot Secondary) | BLE Link to Epcot-Sen-2 | Platform_C2_Speaker | ~46ft | Planned |
| D1-D6 (TTC Grid) | WiFi + Mesh Repeaters 1&2 | Grid_Speakers_D1-D6 | ~25ft avg | Planned |
| E1 (Barn Ops) | WiFi Link to Barn-Sen-1 | Barn_E1_Speaker | ~30ft | Planned |
| E2 (Consolidation) | WiFi Link to Barn-Sen-2 | Barn_E2_Speaker | ~28ft | Planned |

---

## 🔊 Audio Trigger Events by Sensor Type

### **DISTANCE SENSORS (Proximity)**
Triggers when objects/people approach within set distances:

```python
# Audio trigger thresholds
PROXIMITY_ALERTS = {
    "critical_zone": {
        "distance_m": 1.0,
        "audio_trigger": "safety_warning",
        "character": "current_character",
        "volume": 90  # Max for safety
    },
    "caution_zone": {
        "distance_m": 2.5,
        "audio_trigger": "caution_alert",
        "character": "current_character",
        "volume": 80
    },
    "welcome_zone": {
        "distance_m": 5.0,
        "audio_trigger": "welcome_greeting",
        "character": "current_character",
        "volume": 75
    }
}
```

### **SPEED SENSORS (Motion)**
Triggers based on monorail speed:

```python
SPEED_AUDIO_EVENTS = {
    "stationary": {
        "speed_kmh": 0,
        "audio_trigger": "station_boarding",
        "duration_sec": 15
    },
    "departure": {
        "speed_kmh": 0.5,
        "audio_trigger": "departure_chime",
        "duration_sec": 3
    },
    "acceleration": {
        "speed_kmh": 5,
        "audio_trigger": "journey_music_start",
        "duration_sec": 2
    },
    "cruising": {
        "speed_kmh": 20,
        "audio_trigger": "ambient_journey_audio",
        "duration_sec": 300  # Continuous
    },
    "deceleration": {
        "speed_kmh": 15,
        "audio_trigger": "upcoming_station_notice",
        "duration_sec": 5
    }
}
```

### **POSITION SENSORS (Location)**
Triggers based on specific track positions:

```python
POSITION_AUDIO_EVENTS = {
    "monorail_1": {
        "location": "Polynesian_Approach",
        "audio_trigger": "polynesian_welcome",
        "next_station": "Polynesian"
    },
    "monorail_2": {
        "location": "Grand_Floridian_Pass",
        "audio_trigger": "grand_floridian_feature",
        "description_audio": true
    },
    "monorail_3": {
        "location": "Magic_Kingdom_Descent",
        "audio_trigger": "mk_excitement_build",
        "next_station": "Magic_Kingdom"
    }
    # ... (continues for all positions)
}
```

---

## 📊 Audio File Inventory

### **Structure**:
```
Audio_Files/
├── Characters/
│   ├── mickey_mouse/
│   │   ├── announcements/
│   │   ├── safety_reminders/
│   │   ├── seasonal/
│   │   └── ambient/
│   ├── minnie_mouse/
│   ├── cast_member/
│   └── automated/
│
├── Seasonal/
│   ├── holiday_2025/
│   ├── spring_2025/
│   ├── summer_2025/
│   └── fall_2025/
│
├── Sound_Effects/
│   ├── chimes/
│   ├── safety_alerts/
│   ├── door_alerts/
│   └── ambient/
│
└── Ambient/
    ├── journey_music/
    ├── platform_ambience/
    ├── station_themes/
    └── transition_audio/
```

---

## 🔧 Integration with CAD System

### **Audio Speaker Placement Validation**

Each audio speaker must be:
1. **Positioned in CAD model** with precise coordinates
2. **Linked to nearest sensor** (WiFi/BLE coverage check)
3. **Validated for acoustic coverage** (based on space dimensions)
4. **Wired to power and audio systems** (cable routing in CAD)

### **CAD Speaker Objects Template**:
```python
speaker = {
    "id": "Speaker_Zone_A1",
    "type": "audio_speaker",
    "location": "Polynesian_Platform",
    "zone": "A1",
    "position": {"x": 125.4, "y": 85.2, "z": 3.5},  # CAD coordinates
    "mounting": "wall_mount",
    "power_source": "BLE_powered",
    "audio_connection": "WiFi_stream",
    "coverage_radius_m": 15,
    "frequency_response": "100Hz-20kHz",
    "max_volume_db": 95,
    "cad_reference": "Platform_A1_Speaker.blend",
    "linked_sensors": ["Resort_Sensor_1"],
    "validation_status": "pending_cad_integration"
}
```

---

## ⚙️ Control System Integration

### **Audio Trigger Controller**:
```json
{
  "system_config": {
    "central_hub": "TTC_WiFi_Hub",
    "backup_hub": "Barn_WiFi_Hub",
    "update_frequency_hz": 10,
    "audio_latency_ms": 150,
    "mesh_network": {
      "repeater_1": "TTC_Central",
      "repeater_2": "TTC_Secondary",
      "coverage_overlap": "100%"
    }
  },
  
  "audio_playback": {
    "priority_queue": true,
    "max_concurrent_speakers": 6,
    "volume_normalization": true,
    "fade_transitions": 500,  # milliseconds
    "crossfade_enabled": true
  },
  
  "sensor_to_audio_mapping": {
    "distance_sensors": ["warning_audio", "safety_alerts"],
    "speed_sensors": ["journey_audio", "status_updates"],
    "position_sensors": ["destination_audio", "location_announcements"],
    "occupancy_sensors": ["capacity_alerts", "queue_announcements"]
  }
}
```

---

## 🎯 Implementation Roadmap

### **Phase 1: Audio Framework Setup**
- [ ] Define audio file specifications and codec standards
- [ ] Create character audio profiles (Mickey, Minnie, Cast Member, Automated)
- [ ] Generate seasonal audio banks
- [ ] Establish audio delivery system

### **Phase 2: Sensor-to-Audio Integration**
- [ ] Map all 39 sensors to audio trigger events
- [ ] Create trigger condition definitions
- [ ] Develop sensor listener scripts
- [ ] Test audio latency (target: <200ms)

### **Phase 3: CAD Speaker Placement**
- [ ] Design speaker housings for CAD
- [ ] Place speakers in CAD models (all zones A1-E2)
- [ ] Validate acoustic coverage
- [ ] Create wiring diagrams in CAD

### **Phase 4: Mesh Network Configuration**
- [ ] Configure WiFi/BLE mesh network
- [ ] Implement Mesh Repeater 1 and 2
- [ ] Test coverage across all zones
- [ ] Create fallback/redundancy protocols

### **Phase 5: Testing & Validation**
- [ ] Audio trigger event testing
- [ ] Character voice validation
- [ ] Seasonal audio switching
- [ ] Mesh network stability testing
- [ ] Acoustic coverage validation

---

## 📋 Configuration Template (Per Location)

```json
{
  "location_id": "Resort_Monorail_Polynesian",
  "zone": "A1",
  "primary_sensor": "Resort_Sensor_1",
  "speaker_id": "Speaker_Zone_A1",
  "cad_reference": "Platform_A1_Speaker",
  
  "audio_config": {
    "character": "mickey_mouse",
    "season": "holiday",
    "language": "english",
    "volume_level": 75,
    "enabled": true
  },
  
  "trigger_events": [
    {
      "event": "passenger_arrival",
      "audio": "welcome_greeting_holiday_mickey",
      "delay_ms": 500
    },
    {
      "event": "door_opening",
      "audio": "door_alert_safety_reminder",
      "delay_ms": 100
    },
    {
      "event": "monorail_departure",
      "audio": "departure_chime_cheerful",
      "delay_ms": 2000
    },
    {
      "event": "station_approach",
      "audio": "upcoming_station_polynesian",
      "delay_ms": 0
    }
  ],
  
  "mesh_network": {
    "primary_repeater": "Mesh_Repeater_1",
    "backup_repeater": "Mesh_Repeater_2",
    "signal_strength_target_dbm": -65
  }
}
```

---

## 📝 Notes for Wiring Validation

- **CAD overlay**: All audio zones mapped to physical CAD speaker models
- **Sensor alignment**: Each speaker zone linked to nearest sensor for trigger validation
- **Redundancy**: TTC zones have dual mesh repeater coverage
- **Adjustments ready**: Configuration system allows for real-time audio zone modifications
- **Future integration**: System designed to accommodate new characters, seasons, and audio profiles

---

**Status**: Framework Ready for CAD Integration  
**Next Step**: CAD speaker placement and wiring diagram creation  
**Contact**: WDW Monorail System Engineering Team  


