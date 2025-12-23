# WDW Monorail System - Sensor Placement Quick Reference

**Quick lookup guide for sensor locations and functions**

---

## At-a-Glance Sensor Map

```
                    MAGIC KINGDOM
                   (MK Sensor)
                      │
         EXPRESS ──── ┼ ──── RESORT
         (6.5 mi)     │      (8.0 mi loop)
                      │
    CONTEMPORARY   ╱──┼──╲
    (CR Sensor) ──    │    ── GRAND FLORIDIAN
                      │        (GF Sensor)
              
              MONORAIL BARN
           (Barn Sensor)
              │
              └─── MAINTENANCE SPUR (1.5 mi)
                   Junction: Poly + MK
              
    POLYNESIAN ─────╱──────╲
    (Poly Sensor)  /        \
                  /          \
    TRANSPORTATION & TICKET CENTER
         (TTC Sensor)
              │
              │
           EPCOT
        (Epcot Sensor)
        (2.2 mi branch)
```

---

## Station Sensors (7 Total)

### 🔴 RED STATIONS (Hub Junction Points)

| **Sensor** | **Location** | **Lines Served** | **Key Function** |
|---|---|---|---|
| **TTC Sensor** | Transportation & Ticket Center | Express + Resort + Epcot | 3-way hub junction; line selector |
| **MK Sensor** | Magic Kingdom | Express + Resort | 2-way hub junction; line merge |

**Hub Functions:**
- Train arrival/departure sequencing
- Load/unload cycle management
- Line switching and traffic direction
- Peak-hour passenger flow control

---

### 🟢 GREEN STATIONS (Resort Stops - Inner Loop)

| **Sensor** | **Location** | **Line Only** | **Key Function** |
|---|---|---|---|
| **CR Sensor** | Contemporary Resort | Resort Loop | Station dwell timing |
| **GF Sensor** | Grand Floridian | Resort Loop | Station dwell timing |
| **Poly Sensor** | Polynesian Village | Resort Loop + Maintenance | Station stop + Barn access |

**Resort Loop Characteristics:**
- Clockwise routing: TTC → Poly → GF → CR → MK → TTC
- 8.0 miles total loop
- Serve three resort properties
- Poly sensor has dual function (resort + maintenance access)

---

### 🔵 BLUE STATION (Branch Terminus)

| **Sensor** | **Location** | **Line Only** | **Key Function** |
|---|---|---|---|
| **Epcot Sensor** | Epcot | Epcot Line (linear) | Branch terminus; turnaround control |

**Epcot Line Characteristics:**
- Linear branch from TTC
- 2.2 miles out and back
- No intermediate stops
- Dedicated beam line

---

### 🟡 YELLOW STATION (Maintenance)

| **Sensor** | **Location** | **Facility** | **Key Function** |
|---|---|---|---|
| **Barn Sensor** | Monorail Barn | Maintenance Only | Occupancy & access control |

**Barn Characteristics:**
- Not open to public
- Stores up to 10 trains (upper level)
- Accessed via maintenance spur
- Critical for fleet scheduling

---

## Junction Sensors (3 Total)

### TTC Junction (3-Way Split)
```
         ┌─ EXPRESS → Magic Kingdom
    TTC ─┼─ RESORT → Poly/GF/CR/MK/TTC  
         └─ EPCOT → Epcot
```
**Sensor Function:** Line selector switch; traffic director  
**Critical:** Primary hub control point

---

### MK Junction (2-Way Merge)
```
    EXPRESS ───┐
               ├─ COMBINE → MK Platform
    RESORT ────┘
```
**Sensor Function:** Line merge control; collision prevention  
**Critical:** Merge safety at primary hub

---

### Barn Junction (Spur Access)
```
    MAINTENANCE SPUR ───┐
                        ├─ Barn Entry
    (From Poly/MK) ─────┘
```
**Sensor Function:** Maintenance scheduling; spur access control  
**Critical:** Fleet maintenance coordination

---

## Track Segment Sensors (12-15 Total)

### EXPRESS LINE SEGMENTS
```
TTC ─ SENSOR ─ SENSOR ─ SENSOR ─ MK
      1 mi    1.5 mi   2 mi   (6.5 mi total)
```
- **Checkpoint Spacing:** ~1 mile intervals
- **Total Sensors:** 2-3 (plus junctions)
- **Speed Enforcement:** Primary 40 mph maximum zone
- **Collision Prevention:** Emergency override points

---

### RESORT LOOP SEGMENTS
```
TTC ─ Poly ─ GF ─ CR ─ MK ─ (back to TTC)
     ~2mi   ~1.5mi  ~2mi  ~2.5mi
     SENSOR SENSOR SENSOR SENSOR
```
- **Checkpoint Spacing:** ~1.5-2 miles per stop
- **Total Sensors:** 6-8 (distributed around loop)
- **Speed Enforcement:** 30 mph average with station stops
- **Curve Control:** 15-25 mph at transitions

---

### EPCOT BRANCH SEGMENTS
```
TTC ─ SENSOR ─ SENSOR ─ Epcot
     0.5 mi  1.1 mi   (2.2 mi total)
```
- **Checkpoint Spacing:** Linear, ~1 mile
- **Total Sensors:** 2-3 (including junctions)
- **Speed Enforcement:** 35 mph average
- **Branch Safety:** Dedicated line isolation

---

### MAINTENANCE SPUR SEGMENTS
```
Barn ─ SENSOR ─ JUNCTION
       (1.5 mi total)
       └─ Poly junction
       └─ MK junction
```
- **Checkpoint Spacing:** Junction-focused
- **Total Sensors:** 2-3 (access points)
- **Speed Control:** 10-20 mph (maintenance access)
- **Occupancy Tracking:** Barn-specific monitoring

---

## Speed Zone Reference

### Station Platforms
```
Zone:    TTC | STATION | CR | GF | Poly | Epcot | Barn
Speed:   5-10  5-10     5-10 5-10 5-10  5-10   5-10 mph
```

### Approach Zones (0.5 mile before station)
```
Deceleration:  15-25 mph
Control:       Sensor-enforced speed reduction
```

### Main Line Segments
```
Express:  35-40 mph (maximum)
Resort:   30-35 mph (between stops)
Epcot:    30-35 mph (linear)
Maint:    10-20 mph (spur access)
```

### Curve & Transition Zones
```
All elevation curves:  15-25 mph
Track transitions:     20-30 mph
Emergency override:    0-15 mph
```

---

## Sensor Count Summary

| **Type** | **Quantity** | **Locations** |
|---|---|---|
| **Station Sensors** | 7 | TTC, MK, CR, GF, Poly, Epcot, Barn |
| **Junction Sensors** | 3 | TTC Junction, MK Junction, Barn Junction |
| **Track Segment Sensors** | 12-15 | Distributed along all lines |
| **Safety/Emergency Sensors** | Multiple | Platform edges, doors, overrides |
| **Speed Zone Sensors** | Multiple | Boundary enforcement points |
| **TOTAL ACTIVE** | **35-50+** | System-wide coverage |

---

## Critical Sensor Functions

### PRIMARY CONTROL
1. **TTC Sensor** → System hub control
2. **MK Sensor** → Secondary hub control
3. **Junction Sensors** → Traffic direction

### SAFETY ENFORCEMENT
1. **Speed Zone Sensors** → Enforce 5-40 mph limits
2. **Overspeed Detection** → Automatic braking trigger
3. **Collision Avoidance** → Moving Block System integration

### OPERATIONAL MANAGEMENT
1. **Station Sensors** → Load/unload timing
2. **Dwell Sensors** → Stop duration control
3. **Maintenance Sensors** → Barn scheduling

### EMERGENCY RESPONSE
1. **Override Points** → Manual safety intervention
2. **Emergency Brakes** → Automatic activation
3. **Platform Safety** → Edge and door interlocks

---

## Installation Sequence (Recommended)

### Phase 1: Hub Sensors
- TTC Sensor
- MK Sensor
- All Junction Sensors

### Phase 2: Station Sensors
- CR, GF, Poly, Epcot, Barn Sensors

### Phase 3: Track Segments
- Express line sensors
- Resort loop sensors
- Epcot branch sensors

### Phase 4: Safety Systems
- Overspeed detection
- Collision avoidance
- Emergency overrides

### Phase 5: Testing & Calibration
- System integration testing
- Speed zone validation
- Safety protocol verification

---

## Maintenance Notes

**Sensor Inspection Schedule:**
- Station Sensors: Weekly operational checks
- Junction Sensors: Bi-weekly functional tests
- Track Sensors: Monthly calibration verification
- Safety Systems: Quarterly comprehensive audit

**Sensor Backup/Redundancy:**
- Critical hub sensors (TTC, MK): Dual sensors recommended
- Junction sensors: Redundant safety monitoring
- Emergency overrides: Multiple distributed points

---

## Quick Lookup by Function

### "I need to control..."

| **Control Need** | **Primary Sensor** | **Backup/Support** |
|---|---|---|
| Express line traffic | TTC Sensor + MK Sensor | Junction Sensors |
| Resort loop routing | TTC Sensor → Poly/GF/CR/MK Sensors | Loop segment sensors |
| Epcot branch access | TTC Sensor + Epcot Sensor | Branch sensors |
| Maintenance barn | Barn Sensor + Poly Sensor | Barn Junction Sensor |
| Speed enforcement | Track segment sensors | Station approach sensors |
| Collision prevention | Junction Sensors | All track sensors |
| Emergency stop | Override points (8-10) | All safety sensors |

---

## Key Takeaways

✓ **7 Station Sensors** - Primary load points  
✓ **3 Junction Sensors** - Traffic control  
✓ **12-15 Track Sensors** - Continuous monitoring  
✓ **Multiple Safety Sensors** - Overspeed, collision, emergency  
✓ **35-50+ Total Sensors** - Full system coverage  

✓ **3 Operational Lines** - Express, Resort, Epcot  
✓ **14.7 Miles of Track** - All monitored  
✓ **6 Public Stations** - Plus 1 maintenance facility  
✓ **12 Monorail Trains** - 360 capacity each  

✓ **This is BASELINE configuration** - Subject to refinement  
✓ **Safety-first design** - Multiple redundancies  
✓ **Scalable architecture** - Can accommodate future expansion  

---

**Document Status:** BASELINE / QUICK REFERENCE  
**Last Updated:** December 22, 2025

