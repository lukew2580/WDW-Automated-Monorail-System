# Walt Disney World Monorail System
## Baseline Sensor & Track Layout Specification

**Project:** WDW Automated Monorail System  
**Document Type:** Technical Reference - Baseline Configuration  
**Version:** 1.0  
**Date:** December 22, 2025

---

## Executive Summary

This document establishes the **baseline/suggested sensor placement and track layout** for the Walt Disney World Monorail System automation groundwork. This configuration is designed to provide:

- Real-time train position tracking across all three operational lines
- Speed zone enforcement (15-40 mph operational limits)
- Collision avoidance via Moving Block System (MBS/MAPO)
- Station load/unload cycle management
- Maintenance facility access control
- Full safety protocol coverage

**Important Note:** This is a BASELINE layout. It represents the foundational sensor architecture and track configuration based on the existing WDW monorail infrastructure. All specifications are **suggested/proposed** and subject to refinement based on operational testing and system requirements.

---

## System Overview

### Geographic Layout

The Walt Disney World Monorail System consists of **14.7 miles of elevated concrete beam track** serving six public stations plus one maintenance facility. The system operates on two distinct routes with three separate service lines:

| **Component** | **Specification** |
|---|---|
| Total Track Length | 14.7 miles (23.7 km) |
| Public Stations | 6 |
| Maintenance Facility | 1 (Monorail Barn) |
| Active Service Lines | 3 (Express, Resort, Epcot) |
| Monorail Fleet | 12 Mark VI trains |
| Passenger Capacity per Train | 360 people (60 per car) |
| Daily Ridership | 150,000+ passengers |
| Average Operating Speed | 30-40 mph |
| Maximum Operating Speed | 40 mph |
| Operational Hours | 14-17 hours (varies by season) |

---

## Station Locations & Primary Sensors

### 1. Transportation & Ticket Center (TTC)
**Primary Hub - Central Junction Point**

- **Location:** Central transportation hub; serves as entry point to all monorail lines
- **Primary Sensor:** TTC Sensor (Main hub designation)
- **Sensor Functions:**
  - Load/unload detection (all three lines)
  - Track switching control (Express/Resort/Epcot selector)
  - Train arrival/departure sequencing
  - Passenger flow monitoring
- **Connected Lines:** Express, Resort, Epcot
- **Distance to MK:** 6.5 miles (Express) / 8.0 miles (Resort)
- **Distance to Epcot:** 2.2 miles

### 2. Magic Kingdom
**Main Destination Hub**

- **Location:** Inside Magic Kingdom Park; main transportation nexus
- **Primary Sensor:** MK Sensor (Main hub designation)
- **Sensor Functions:**
  - Load/unload detection
  - Express/Resort line merge point
  - Maintenance spur connection
  - Peak-hour traffic management
- **Connected Lines:** Express, Resort
- **Lines Converge Here:** Both Express and Resort lines service this station
- **Critical Junction:** Connection to Monorail Barn maintenance facility

### 3. Disney's Contemporary Resort
**Resort Stop - Inner Loop (Clockwise)**

- **Location:** Along Seven Seas Lagoon; resort guest transportation
- **Primary Sensor:** CR Sensor (Resort line exclusive)
- **Sensor Functions:**
  - Load/unload detection
  - Dwell time monitoring
  - Resort-specific traffic control
- **Connected Line:** Resort Line only
- **Position:** Upper right of system loop
- **Distance from TTC:** ~5.5 miles (clockwise via Poly/GF)

### 4. Disney's Grand Floridian Resort & Spa
**Resort Stop - Inner Loop (Clockwise)**

- **Location:** Along Seven Seas Lagoon; resort guest transportation
- **Primary Sensor:** GF Sensor (Resort line exclusive)
- **Sensor Functions:**
  - Load/unload detection
  - Dwell time monitoring
  - Resort-specific traffic control
- **Connected Line:** Resort Line only
- **Position:** Right side of system loop
- **Distance from TTC:** ~4.0 miles (clockwise via Poly)

### 5. Disney's Polynesian Village Resort
**Resort Stop - Inner Loop (Clockwise)**

- **Location:** Along Seven Seas Lagoon; resort guest transportation
- **Primary Sensor:** Poly Sensor (Resort line + Maintenance access)
- **Sensor Functions:**
  - Load/unload detection
  - Dwell time monitoring
  - Maintenance spur access control (connection to Barn)
  - Resort-specific traffic control
- **Connected Line:** Resort Line + Maintenance Spur
- **Position:** Lower left of system loop
- **Distance from TTC:** ~2.0 miles (clockwise)
- **Critical Function:** Maintenance spur junction point

### 6. Epcot
**Branch Terminus - Linear Extension**

- **Location:** Outside Epcot Park; guest transportation hub
- **Primary Sensor:** Epcot Sensor (Epcot line exclusive)
- **Sensor Functions:**
  - Load/unload detection
  - Linear branch terminus control
  - Epcot line turnaround sequencing
- **Connected Line:** Epcot Line only
- **Position:** Left extension from TTC
- **Distance from TTC:** 2.2 miles (linear branch)

### 7. Monorail Barn
**Maintenance & Storage Facility - Not Open to Public**

- **Location:** Short distance northeast of Magic Kingdom
- **Primary Sensor:** Barn Sensor (Facility access control)
- **Sensor Functions:**
  - Train occupancy detection
  - Storage position tracking
  - Maintenance cycle coordination
  - Spur track access control
- **Connected Line:** Maintenance Spur only
- **Upper Level:** Storage for up to 10 Mark VI trains
- **Lower Level:** Walt Disney World Railroad facility + vehicle maintenance
- **Critical Function:** Maintenance scheduling and fleet management

---

## Track Layout & Service Lines

### LINE 1: EXPRESS LINE (Red)
**Direct TTC ↔ Magic Kingdom Service**

```
TTC ======================== MK
(6.5 miles - Outer Loop - Non-stop)
```

**Specifications:**
- **Route:** Outer loop - direct routing
- **Distance:** 6.5 miles
- **Stops:** 2 (TTC + Magic Kingdom)
- **Average Speed:** 40 mph (maximum operational speed)
- **Travel Time:** 8-10 minutes
- **Service Pattern:** Nonstop express service
- **Beam Configuration:** Standard outer beam track

**Sensor Placement:**
- TTC Station Sensor (Platform detection)
- TTC Junction Point (Line selector switch)
- Mid-track Checkpoint (~3.25 miles from TTC)
- MK Station Sensor (Platform detection)
- MK Junction Point (Line merge)
- Emergency Override Sensors (2 locations)

**Speed Zones:**
- TTC Platform: 10-15 mph
- Main Line: 35-40 mph
- MK Approach: 15-25 mph
- MK Platform: 5-10 mph

---

### LINE 2: RESORT LINE (Green)
**Circular Loop - TTC → Polynesian → Grand Floridian → Contemporary → MK → TTC**

```
TTC ─→ Poly ─→ GF ─→ CR ─→ MK ─→ TTC
(8.0 miles - Inner Loop - Clockwise)
```

**Specifications:**
- **Route:** Inner loop - clockwise circulation
- **Distance:** 8.0 miles (full loop)
- **Stops:** 5 (TTC, Poly, GF, CR, MK, back to TTC)
- **Average Speed:** 30 mph (includes dwell times)
- **Travel Time:** 15-17 minutes
- **Service Pattern:** Continuous loop with all resort stops
- **Beam Configuration:** Inner beam track throughout

**Sensor Placement:**
- TTC Station Sensor (Platform detection)
- Polynesian Station Sensor (Platform detection)
- Grand Floridian Station Sensor (Platform detection)
- Contemporary Resort Station Sensor (Platform detection)
- Magic Kingdom Station Sensor (Platform detection)
- TTC-Poly Junction (Line selector)
- Poly-GF Junction (Curve control)
- GF-CR Junction (Curve control)
- CR-MK Junction (Curve control)
- MK-TTC Junction (Curve control)
- Curve/Transition Sensors (6-8 locations around loop)

**Speed Zones:**
- Station Platforms: 5-10 mph
- Between-Station Segments: 30-35 mph
- Curve Sections: 15-25 mph

---

### LINE 3: EPCOT LINE (Blue)
**Linear Branch - TTC ↔ Epcot**

```
TTC ════════════════════ Epcot
(2.2 miles - Linear Branch)
```

**Specifications:**
- **Route:** Linear branch - straight outbound/return
- **Distance:** 2.2 miles
- **Stops:** 2 (TTC + Epcot)
- **Average Speed:** 35 mph
- **Travel Time:** 4-5 minutes
- **Service Pattern:** Single beam linear routing
- **Beam Configuration:** Dedicated linear extension

**Sensor Placement:**
- TTC Station Sensor (Platform detection)
- TTC-Epcot Junction Point (Branch connection)
- Mid-track Checkpoint (~1.1 miles from TTC)
- Epcot Station Sensor (Platform detection)
- Emergency Override Sensors (2 locations)

**Speed Zones:**
- TTC Platform: 10-15 mph
- Epcot Branch: 30-35 mph
- Epcot Approach: 15-25 mph
- Epcot Platform: 5-10 mph

---

### MAINTENANCE SPUR (Yellow)
**Non-Public Access - Barn ↔ Main Loop**

```
          Barn
            │
            │ (1.5 miles)
            │
    Poly ───┼─── MK
    (Junction Connection Points)
```

**Specifications:**
- **Route:** Spur access track to maintenance facility
- **Distance:** ~1.5 miles total (Barn → Poly junction + Barn → MK connection)
- **Access Points:** 2 (Polynesian junction + Magic Kingdom junction)
- **Service Pattern:** On-demand access for maintenance cycles
- **Occupancy:** 10 trains maximum (upper level of Barn)

**Sensor Placement:**
- Barn Entry/Exit Sensor (Occupancy detection)
- Barn-Poly Junction Sensor (Spur control)
- Barn-MK Junction Sensor (Spur control)
- Emergency track sensors (2-3 locations)
- Maintenance scheduling sensors

---

## Comprehensive Sensor Deployment Reference

### PRIMARY STATION SENSORS (7 Total)

| **Sensor ID** | **Location** | **Connected Line(s)** | **Primary Functions** |
|---|---|---|---|
| TTC Sensor | Transportation & Ticket Center | Express, Resort, Epcot | Hub control, line switching, load/unload detection |
| MK Sensor | Magic Kingdom | Express, Resort | Hub control, line merge, load/unload detection |
| CR Sensor | Contemporary Resort | Resort | Station stop, load/unload detection, dwell timing |
| GF Sensor | Grand Floridian | Resort | Station stop, load/unload detection, dwell timing |
| Poly Sensor | Polynesian Village | Resort + Maintenance | Station stop, maintenance access, load/unload |
| Epcot Sensor | Epcot | Epcot | Branch terminus, turnaround sequencing |
| Barn Sensor | Monorail Barn | Maintenance | Occupancy detection, storage tracking |

### JUNCTION CONTROL SENSORS (3 Total)

| **Junction** | **Connected Lines** | **Control Functions** | **Critical Functions** |
|---|---|---|---|
| TTC Junction | Express/Resort/Epcot split point | Line selector switch, traffic director | 3-way traffic control at main hub |
| MK Junction | Express/Resort merge point | Line merge control, traffic sequencing | Collision avoidance at merge point |
| Barn Junction | Maintenance spur connection | Spur access control, maintenance scheduling | Barn access authorization |

### TRACK SEGMENT SENSORS (12-15 Total)

**Purpose:** Continuous position tracking and speed zone enforcement

- **Express Line Segments:** 2-3 sensors (including mid-point checkpoint)
- **Resort Loop Segments:** 6-8 sensors (one per ~1-1.5 mile segment)
- **Epcot Line Segments:** 2-3 sensors (including mid-point checkpoint)
- **Curve/Transition Points:** 6-8 distributed across system
- **Speed Zone Boundaries:** Multiple enforcement points
- **Collision Avoidance Points:** All junction areas and high-risk zones

**Sensor Spacing Guidelines:**
- Express Line: ~1 mile intervals
- Resort Loop: ~1.5-2 miles per stop
- Epcot Line: ~1 mile intervals
- Maintenance Spur: Junction points + access control

### SAFETY & EMERGENCY SENSORS (Multiple Distributed)

**Critical Safety Infrastructure:**

- **Platform Edge Sensors:** All 6 stations (passenger boundary detection)
- **Door Interlock Sensors:** All 6 stations (door safety interlocks)
- **Overspeed Detection:** All track segments (speed enforcement)
- **Collision Avoidance:** All junction points (train separation)
- **Emergency Override Points:** Minimum 8-10 distributed locations
- **Moving Block System (MBS) Sensors:** Continuous track monitoring

---

## Speed Zone Mapping

### Operational Speed Limits

| **Zone Type** | **Speed Range** | **Applications** |
|---|---|---|
| Platform/Loading Areas | 5-10 mph | All station platforms |
| Station Approach | 15-25 mph | Final 0.5 mile to each station |
| Curve/Transition Zones | 15-25 mph | All elevated curves and transitions |
| Main Line Sections | 30-40 mph | Between-station straight segments |
| Emergency/Safety | 0-15 mph | Override and emergency situations |

**Key Speed Enforcement Points:**
1. TTC Platform: 5-10 mph (hub congestion control)
2. Resort Loop Transitions: 15-25 mph (passenger safety at stops)
3. Express Main Beam: 35-40 mph (maximum speed maintenance)
4. Epcot Branch: 30-35 mph (linear routing efficiency)
5. Maintenance Spur: 10-20 mph (controlled access)

---

## Moving Block System (MBS) Integration

**System Name:** MAPO (Mary Poppins - Disney's playful acronym)

**Function:** Automated train spacing and collision prevention

**Sensor Architecture:**
- Establishes "holdpoints" throughout the system
- Maintains minimum 2 holdpoints between consecutive trains
- Triggers emergency brakes if spacing violation occurs
- Cannot be overridden without operator authorization
- Integral to all track segments

**Critical Points:**
- Every sensor location functions as a potential holdpoint
- Spacing violations classified as "overrun" (critical safety issue)
- System prioritizes passenger safety over schedule adherence

---

## Implementation Considerations

### Phase 1: Foundation (This Document)
- Baseline sensor placement mapping
- Track layout confirmation
- Station identification and sensor allocation
- Critical junction mapping

### Phase 2: Testing & Refinement
- Sensor installation and calibration
- Track system testing
- Speed zone validation
- Emergency protocol verification

### Phase 3: Operational Deployment
- Full system integration
- Operator training
- Passenger safety testing
- Real-world performance monitoring

### Phase 4: Optimization
- Sensor adjustment based on operational data
- Fine-tuning of speed zones
- Enhanced safety protocols
- System efficiency improvements

---

## Key Specifications Summary

**Total System Metrics:**
- **Track:** 14.7 miles
- **Stations:** 6 public + 1 maintenance facility
- **Lines:** 3 (Express, Resort, Epcot)
- **Trains:** 12 Mark VI monorails
- **Capacity:** 360 passengers per train
- **Daily Ridership:** 150,000+
- **Operating Hours:** 14-17 hours daily

**Sensor Deployment:**
- **Station Sensors:** 7
- **Junction Sensors:** 3
- **Track Segment Sensors:** 12-15
- **Safety Sensors:** Multiple distributed
- **Total Active Sensors:** 35-50+ (varies by phase)

**Track Configuration:**
- **Express Line:** 6.5 miles outer loop (2 stops)
- **Resort Line:** 8.0 miles inner loop (5 stops)
- **Epcot Line:** 2.2 miles linear branch (2 stops)
- **Maintenance Spur:** 1.5 miles access track

---

## Safety Protocols

### Emergency Features
1. **Overspeed Prevention:** Automatic speed enforcement via sensors
2. **Collision Avoidance:** Moving Block System with automatic braking
3. **Platform Safety:** Edge and door interlocks
4. **Manual Override:** Pilot cab override capability (emergency only)
5. **System Shutdown:** Emergency stop available at all stations and override points

### Operator Controls
- Automated platform dispatch via control panels
- Real-time train monitoring
- Manual override capability (supervised pilots)
- Emergency response protocols
- Communication systems

---

## Final Notes

This **BASELINE/SUGGESTED layout** represents the foundational sensor architecture and track configuration for the WDW Monorail System. The specifications are based on:

- Existing monorail infrastructure analysis
- Real-world Disney operational requirements
- Safety protocol integration
- Passenger capacity management
- Maintenance facility access

**Status:** This is a working reference document for system planning and design. All details are subject to refinement based on actual site conditions, operational testing, and specific project requirements.

---

**Document Prepared:** December 22, 2025  
**Status:** BASELINE / SUGGESTED CONFIGURATION  
**Classification:** Reference Material for WDW Automated Monorail System Project

