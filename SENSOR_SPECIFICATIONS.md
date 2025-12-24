# WDW Monorail System - Sensor Specifications

## Overview
This document outlines the specific sensor models and specifications for the hybrid WiFi/Bluetooth mesh network architecture supporting the WDW Automated Monorail System.

## Track Layer Sensors (WiFi-Enabled)

### Recommended WiFi Sensors

#### 1. **Proximity Sensors - WiFi**
- **Model**: Shelly Plus H&T (Humidity & Temperature)
  - Protocol: WiFi 2.4GHz/5GHz
  - Range: Up to 100m (open space)
  - Power: PoE or USB-C
  - API: REST/MQTT
  - Cost: ~$25-35 per unit
  - Use Case: Track position detection, environmental monitoring

- **Model**: Tuya Smart WiFi Ultrasonic Sensor
  - Protocol: WiFi 2.4GHz
  - Detection Range: 0.2-6 meters (configurable)
  - Power: Battery (AA) or USB powered
  - API: MQTT/REST
  - Cost: ~$15-25 per unit
  - Use Case: Monorail position detection on track

#### 2. **Environmental Sensors - WiFi**
- **Model**: Aqara Smart Temperature & Humidity Sensor (WiFi)
  - Protocol: WiFi ZigBee gateway required or WiFi direct
  - Accuracy: ±0.5°C, ±5% RH
  - Power: PoE optional
  - API: MQTT
  - Cost: ~$30-40 per unit
  - Use Case: Barn temperature, humidity monitoring for equipment protection

- **Model**: Eve Outdoor Cam (WiFi)
  - Protocol: WiFi 2.4GHz/5GHz
  - Detection: Motion, Light level
  - Power: PoE or Battery
  - API: HomeKit/REST
  - Cost: ~$50-70 per unit
  - Use Case: Visual monitoring, motion detection for automation triggers

#### 3. **Motion Sensors - WiFi**
- **Model**: Tuya Smart PIR WiFi Motion Sensor
  - Protocol: WiFi 2.4GHz
  - Detection Range: 5-8 meters
  - Power: Battery (AA) or PoE
  - API: MQTT
  - Cost: ~$12-18 per unit
  - Use Case: Barn activity detection, automation triggers

## Monorail Layer (Bluetooth Low Energy)

### Recommended BLE Modules

#### 1. **BLE Beacon/Transmitter**
- **Model**: Adafruit Bluefruit LE UART Friend
  - Protocol: Bluetooth 4.0 Low Energy
  - Range: 20-30 meters (line of sight)
  - Power: Rechargeable LiPo battery (3.7V)
  - Dimensions: Compact, fits in monorail unit
  - Cost: ~$25-30 per unit
  - Use Case: Monorail identification and location tracking

- **Model**: nRF52840 DK (Nordic Semiconductor)
  - Protocol: Bluetooth 5.0
  - Range: Up to 240 meters (with antenna)
  - Power: USB or Battery powered
  - Dimensions: Development board (can be miniaturized)
  - Cost: ~$40 per unit
  - Use Case: Advanced BLE mesh networking, monorail coordination

#### 2. **BLE Proximity Sensors**
- **Model**: Tile Slim 2025
  - Protocol: Bluetooth 5.3
  - Range: 200+ feet (60+ meters)
  - Power: Replaceable battery (3-year life)
  - Dimensions: Slim, fits easily in monorail
  - Cost: ~$25 per unit
  - Use Case: Simple proximity tracking, location-based audio triggers

#### 3. **Custom BLE Gateway for Monorails**
- **Option**: Raspberry Pi Zero W with BLE Hat
  - Protocol: Bluetooth 5.0 (with compatible HAT)
  - Range: 50-100 meters
  - Power: USB-C (4V, 2.5A)
  - Dimensions: Credit card size
  - Cost: ~$35-50 (Pi Zero W + BLE HAT)
  - Use Case: Advanced control, multi-monorail coordination

## Audio Distribution Layer (Hybrid Mesh - WiFi/BLE)

### Recommended Wireless Speakers

#### 1. **WiFi-Enabled Speakers**
- **Model**: Sonos One (WiFi)
  - Protocol: WiFi 2.4GHz/5GHz + Mesh
  - Power: AC outlet
  - Range: Whole-house mesh (can extend to outdoor)
  - API: REST/MQTT
  - Cost: ~$100-150 per unit
  - Use Case: Premium audio distribution, synchronized playback

- **Model**: LIFX Cync Smart Bulbs with Audio
  - Protocol: WiFi 2.4GHz/5GHz
  - Power: E27/E14 standard fitting
  - Range: 100+ feet with mesh
  - API: REST
  - Cost: ~$40-60 per unit
  - Use Case: Integrated lighting + sound at key locations

- **Model**: Shelly Plus i4 with Relay + Audio Jack
  - Protocol: WiFi 2.4GHz/5GHz
  - Power: PoE or AC powered
  - Audio Output: 3.5mm jack to external amplifier/speaker
  - API: REST/MQTT
  - Cost: ~$25-35 per unit
  - Use Case: Control + audio trigger to passive speakers

#### 2. **BLE Mesh-Compatible Speakers**
- **Model**: IKEA DIRIGERA Hub + LEPTITER Speakers
  - Protocol: Bluetooth Mesh + WiFi
  - Power: AC powered (hub), Battery/AC (speakers)
  - Range: 100+ meters with mesh
  - Cost: ~$50-80 per unit (hub), ~$30-50 (speakers)
  - Use Case: Budget-friendly mesh audio distribution

- **Model**: Philips Hue Play (WiFi + Optional BLE Mesh)
  - Protocol: WiFi 2.4GHz/5GHz + Bluetooth Mesh capable
  - Power: AC powered
  - Range: Home-wide mesh
  - API: REST
  - Cost: ~$80-120 per unit
  - Use Case: Synchronized lighting + audio effects

#### 3. **Passive Speaker System with WiFi Relay**
- **Setup**: 
  - WiFi-controlled audio relay (Shelly device)
  - Passive speakers (wired to relay)
  - Budget: ~$50-100 per location
  - Use Case: Cost-effective, high-quality audio without WiFi on each speaker

## Mesh Network Infrastructure

### WiFi Mesh Nodes
- **Model**: TP-Link Deco M9 Plus or Ubiquiti UniFi
  - Purpose: Extend WiFi coverage across large layout
  - Cost: ~$50-150 per node
  - Coverage: 1,500+ sq ft per node

### Bluetooth Mesh Repeaters
- **Model**: Custom nRF52840 mesh repeater nodes
  - Purpose: Extend BLE range between monorails and track sensors
  - Cost: ~$40-60 per repeater
  - Placement: Strategic points around track

## Central Backend (Raspberry Pi)

### Hardware
- **Raspberry Pi 4 (8GB RAM minimum)**
  - Dual WiFi bands (2.4GHz/5GHz)
  - Integrated Bluetooth 5.0
  - GPIO pins for direct sensor integration
  - Cost: ~$75-100

### BLE Support
- **Built-in Bluetooth**: Supports BLE scanning and gateway functionality
- **Optional HAT**: Waveshare BLE HAT for extended range
  - Cost: ~$25-30

### Networking
- **WiFi**: Direct connection to mesh network
- **Wired Ethernet**: Optional for stability and PoE option

## Summary Table

| Layer | Device Type | Protocol | Quantity (Per Loop) | Cost Per Unit |
|-------|------------|----------|-------------------|--------------|
| Track | Proximity Sensor | WiFi | 3-5 | $15-35 |
| Track | Environmental Sensor | WiFi | 2-3 | $30-40 |
| Track | Motion Sensor | WiFi | 2 | $12-18 |
| Monorail | BLE Beacon | BLE 4.0/5.0 | 3 | $25-40 |
| Monorail | Proximity Tag | BLE 5.3 | 3 | $25 |
| Audio | WiFi Speaker | WiFi Mesh | 4-6 | $40-150 |
| Audio | BLE Mesh Speaker | BLE Mesh | 2-3 | $30-80 |
| Infrastructure | Mesh Repeater | BLE/WiFi | 2-3 | $25-60 |
| Backend | Raspberry Pi 4 | WiFi/BLE | 1 | $75-100 |

## Notes
- All devices should support MQTT or REST API for integration with Raspberry Pi
- Consider PoE (Power over Ethernet) for track sensors to reduce wiring complexity
- BLE range can be extended significantly with mesh topology
- WiFi mesh provides stability; BLE provides real-time location data
- Total estimated cost per basic setup: $400-600


