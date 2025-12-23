# 🎤 Voice and Wiring System Documentation

## 🎯 Overview

This document describes the voice announcements and wiring logic for the WDW Automated Monorail System. It covers station announcements, safety alerts, and the underlying wiring logic for hardware integration.

---

## 📢 Voice Announcements

### Station Announcements

Voice announcements are triggered at specific stations to inform passengers about their current location, upcoming stops, and safety information. The announcements are synchronized with the monorail's position and speed.

#### Announcement Types

1. **Arrival Announcements**
   - Triggered when a monorail arrives at a station.
   - Example: "Welcome to Magic Kingdom. Please watch your step as you exit the monorail."

2. **Departure Announcements**
   - Triggered when a monorail is about to depart from a station.
   - Example: "Next stop: Epcot. Please hold on to your belongings."

3. **Safety Announcements**
   - Triggered during critical events or emergencies.
   - Example: "Attention: The monorail is slowing down due to a safety alert. Please remain seated."

4. **Transfer Announcements**
   - Triggered at transfer stations to guide passengers.
   - Example: "This is the Transportation and Ticket Center. Please transfer here for the Resort Line."

---

## 🔌 Wiring Logic

### Hardware Integration

The wiring logic is managed by the `raspberry_pi_integration.py` module, which controls the GPIO pins on the Raspberry Pi. The wiring logic ensures that the monorail system operates smoothly and safely.

#### Key Components

1. **Motor Control**
   - Managed via L298N motor drivers.
   - Each monorail has dedicated GPIO pins for motor control (e.g., GPIO 17, 27, 22 for Monorail Red).

2. **Sensor Input**
   - Proximity and position sensors are connected to specific GPIO pins (e.g., GPIO 4 for TTC Sensor).
   - Sensors provide real-time feedback on monorail position and speed.

3. **Track Switches**
   - Controlled via GPIO pins (e.g., GPIO 20 for TTC↔MK Switch).
   - Switches are used to route monorails between different lines.

4. **Emergency Stop Relay**
   - Connected to a dedicated GPIO pin.
   - Triggers a hard stop for all monorails in case of an emergency.

---

## 🔄 Event Flow

### Monorail Movement

1. **Departure**
   - The monorail departs from a station.
   - The departure announcement is triggered.
   - The motor control is activated, and the monorail accelerates to the desired speed.

2. **En Route**
   - The monorail travels along the track.
   - Sensors provide real-time feedback on position and speed.
   - The collision avoidance system monitors the track and adjusts speed as needed.

3. **Arrival**
   - The monorail approaches a station.
   - The arrival announcement is triggered.
   - The motor control decelerates the monorail, and it comes to a stop at the station.

4. **Transfer**
   - At transfer stations, the transfer announcement is triggered.
   - Track switches are activated to route the monorail to the correct line.

---

## 🚨 Safety Protocols

### Emergency Stop

1. **Trigger**
   - An emergency stop can be triggered manually via the dashboard or automatically by the collision avoidance system.

2. **Execution**
   - The emergency stop relay is activated.
   - All monorails come to an immediate stop.
   - A safety announcement is triggered: "Attention: Emergency stop activated. Please remain seated."

3. **Recovery**
   - The system checks for the cause of the emergency stop.
   - Once the issue is resolved, the system resumes normal operation.

---

## 📊 Example Scenarios

### Scenario 1: Normal Operation

1. **Departure from TTC**
   - Announcement: "Welcome aboard the WDW Monorail. Next stop: Magic Kingdom."
   - Motor control activates, and the monorail departs.

2. **En Route to MK**
   - Sensors monitor position and speed.
   - Collision avoidance system ensures safe distance from other monorails.

3. **Arrival at MK**
   - Announcement: "Welcome to Magic Kingdom. Please watch your step as you exit."
   - Motor control decelerates, and the monorail stops at the station.

### Scenario 2: Emergency Stop

1. **Collision Imminent**
   - Collision avoidance system detects a potential collision.
   - Announcement: "Attention: Emergency stop activated. Please remain seated."
   - Emergency stop relay activates, and all monorails stop immediately.

2. **Recovery**
   - System checks for the cause of the emergency stop.
   - Once resolved, the system resumes normal operation.

---

## 🔧 Maintenance and Troubleshooting

### Common Issues

1. **Motor Control Failure**
   - Check GPIO pin connections.
   - Verify motor driver functionality.

2. **Sensor Malfunction**
   - Check sensor connections.
   - Verify sensor calibration.

3. **Track Switch Issues**
   - Check GPIO pin connections for track switches.
   - Verify switch functionality.

4. **Voice Announcement Problems**
   - Check audio output connections.
   - Verify announcement triggers in the code.

---

## 📝 Notes

- Always ensure that the wiring logic is correctly configured before operating the monorail system.
- Regularly test the emergency stop functionality to ensure safety.
- Update the voice announcements as needed to provide clear and accurate information to passengers.

