# WDW Monorail System - System Architecture Refinement

## Overview
This document outlines the refined system architecture for the WDW Monorail System, focusing on the integration of multiple subsystems and their coordination under a master system. Each subsystem operates as its own "brain," with specific responsibilities and functionalities, while the master system ensures seamless coordination and communication across all subsystems.

## System Architecture

### 1. **Master System**
The master system acts as the central coordinator, overseeing all subsystems and ensuring seamless communication and coordination. It is responsible for:
- **Overall Coordination:** Managing the interaction between all subsystems.
- **Resource Allocation:** Allocating resources and prioritizing tasks across subsystems.
- **Data Integration:** Integrating data from all subsystems to provide a comprehensive view of the entire monorail system.
- **Decision Making:** Making high-level decisions based on data from all subsystems.

### 2. **Subsystems**
Each subsystem operates as its own "brain," with specific responsibilities and functionalities. The subsystems include:

#### **Barn System**
- **Responsibilities:**
 - Managing the storage and maintenance of monorail vehicles.
 - Coordinating the movement of monorails in and out of the barn.
 - Ensuring the barn's infrastructure is maintained and operational.
- **Components:**
 - Barn motors and actuators.
 - Barn sensors and monitoring systems.
 - Barn control and communication systems.

#### **Track System (Resort and Magic Kingdom Lines)**
- **Responsibilities:**
 - Managing the movement of monorails on the Resort and Magic Kingdom lines.
 - Coordinating the routing of monorails between the Express loop, Resort loop, and barn spur.
 - Ensuring the track infrastructure is maintained and operational.
- **Components:**
 - Track motors and actuators.
 - Track sensors and monitoring systems.
 - Track control and communication systems.

#### **Epcot Express Monorail System**
- **Responsibilities:**
 - Managing the movement of monorails on the Epcot Express line.
 - Coordinating the routing of monorails between the Epcot Express loop and other lines.
 - Ensuring the Epcot Express infrastructure is maintained and operational.
- **Components:**
 - Epcot Express motors and actuators.
 - Epcot Express sensors and monitoring systems.
 - Epcot Express control and communication systems.

#### **Individual Monorail Systems**
- **Responsibilities:**
 - Managing the movement and operation of individual monorail vehicles.
 - Ensuring the safety and comfort of passengers.
 - Coordinating with other subsystems for routing and maintenance.
- **Components:**
 - Monorail motors and actuators.
 - Monorail sensors and monitoring systems.
 - Monorail control and communication systems.

## Communication and Coordination

### 1. **Mesh Network**
The mesh network ensures reliable and redundant communication between all subsystems and the master system. It is responsible for:
- **Real-Time Communication:** Enabling real-time communication between all subsystems.
- **Data Synchronization:** Ensuring data synchronization across all subsystems.
- **Redundancy:** Providing redundancy to ensure continuous operation in case of failures.

### 2. **Master System Coordination**
The master system coordinates the interaction between all subsystems, ensuring seamless operation and efficient resource allocation. It is responsible for:
- **Task Prioritization:** Prioritizing tasks and allocating resources based on the needs of each subsystem.
- **Conflict Resolution:** Resolving conflicts and ensuring smooth operation across all subsystems.
- **Data Integration:** Integrating data from all subsystems to provide a comprehensive view of the entire monorail system.

## Implementation Plan

### 1. **Master System Development**
- **Central Coordinator:** Develop the central coordinator to manage the interaction between all subsystems.
- **Resource Allocation:** Implement resource allocation algorithms to prioritize tasks and allocate resources efficiently.
- **Data Integration:** Develop data integration mechanisms to provide a comprehensive view of the entire monorail system.

### 2. **Subsystem Development**
- **Barn System:** Develop the barn system to manage the storage and maintenance of monorail vehicles.
- **Track System:** Develop the track system to manage the movement of monorails on the Resort and Magic Kingdom lines.
- **Epcot Express System:** Develop the Epcot Express system to manage the movement of monorails on the Epcot Express line.
- **Individual Monorail Systems:** Develop individual monorail systems to manage the movement and operation of individual monorail vehicles.

### 3. **Mesh Network Development**
- **Real-Time Communication:** Implement real-time communication mechanisms to enable seamless communication between all subsystems.
- **Data Synchronization:** Develop data synchronization mechanisms to ensure data consistency across all subsystems.
- **Redundancy:** Implement redundancy mechanisms to ensure continuous operation in case of failures.

### 4. **Master System Coordination**
- **Task Prioritization:** Implement task prioritization algorithms to ensure efficient resource allocation.
- **Conflict Resolution:** Develop conflict resolution mechanisms to ensure smooth operation across all subsystems.
- **Data Integration:** Implement data integration mechanisms to provide a comprehensive view of the entire monorail system.

## Conclusion
The refined system architecture for the WDW Monorail System ensures seamless coordination and communication between all subsystems, providing a comprehensive and efficient monorail system. By developing each subsystem as its own "brain" and coordinating their interaction under a master system, the WDW Monorail System can operate smoothly and efficiently, providing a better experience for passengers and staff alike. The implementation plan provides a roadmap for further development and enhancement, ensuring that the WDW Monorail System continues to evolve and meet the needs of passengers and staff alike.

---

## v1.1 Roadmap: Dual-Radio Communications Architecture

**Status:** Planned for v1.1. This is documentation and a reserved config flag only. No WiFi networking code is implemented yet.

### Background: v1 is Bluetooth-only for trains and track
In v1, all mobile monorail units (trains) and mainline track segments communicate over **Bluetooth only**. This decision stands and does not change: trains are mobile, power-conscious units for which Bluetooth pairing and low-energy operation are the right fit. WiFi is not used on any train or mainline track node.

### The barn is a different class of installation
The monorail **barn** (where trains are stored and serviced) is functionally different from the mainline:
- It is a large, fixed facility with many track switches, motors, and sensors spread across a wide area.
- Its nodes are **fixed infrastructure**, not mobile train units.
- Bluetooth's effective range and practical pairing-count limits make it impractical to reliably cover the barn's dense, spread-out node population from the hub's Bluetooth radio.

### v1.1 design: optional WiFi for barn nodes only
For v1.1, the **hub daemon** (Raspberry Pi 5) will become dual-radio aware and support an optional WiFi radio mode scoped **specifically to barn sensor/motor nodes**:
- **Trains + mainline track segments:** Bluetooth only. No change. WiFi is never used for mobile units.
- **Barn fixed sensor/motor nodes:** may optionally use WiFi, where Bluetooth range/pairing does not scale.
- The hub daemon continues to manage Bluetooth for trains/track while optionally bridging barn fixed nodes over WiFi when the feature is enabled.

### Config flag
A reserved flag `barn_wifi_enabled` (default `false`) gates this behavior and stays off until the WiFi path is actually implemented. See `Configuration/hub_daemon.yml`.

### Out of scope for this documentation change
- No actual WiFi networking / transport code.
- No change to train or mainline track comms (Bluetooth-only is preserved).
- No dashboard changes.
