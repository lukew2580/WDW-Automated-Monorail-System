# WDW Automated Monorail System

A digital-twin and automation system for a Walt Disney World monorail model railway, built to run on Raspberry Pi hardware. The project combines historically accurate 3D CAD models, a distributed sensor network, and a Python automation stack for fleet management, monitoring, and operations.

> **Status:** Approaching v1 release. The functional v1 control dashboard (`dashboard_v1.html`) is merged and live. See [`ROADMAP_2026.md`](ROADMAP_2026.md) and [`README_2026.md`](README_2026.md) for the full status report and history.

## Overview

- **Fleet:** 12 active Mark VI monorail vehicles (2 retired: Pink and Purple), historically accurate 2025 color schemes
- **Stations:** 4 major stations (Polynesian, Grand Floridian, Contemporary, Epcot)
- **Sensor network:** 39 sensors across vehicles, stations, and infrastructure
- **3D models:** CAD models for all vehicles and stations (Blender, with an in-progress CadQuery migration)
- **Automation:** Python-based control, monitoring, and motor/actuator integration

## Hardware & Architecture

The system targets a Raspberry Pi 5 central hub with distributed Raspberry Pi Pico / Pico 2 (RP2040 / RP2350) nodes at track segments and on train cars.

- **Hub (Raspberry Pi 5):** runs the core service handling track state, sensor polling, and command dispatch
- **Nodes (Pico / Pico 2):** motor control, switch actuation, and sensor reads at the edge

Detailed hardware and backend notes:
- [`Documentation/RASPBERRY_PI_SETUP.md`](Documentation/RASPBERRY_PI_SETUP.md)
- [`RASPBERRY_PI_BACKEND_ARCHITECTURE.md`](RASPBERRY_PI_BACKEND_ARCHITECTURE.md)
- [`Documentation/System_Architecture_Refinement.md`](Documentation/System_Architecture_Refinement.md)

## Communications

The v1 communications design uses two radios for two different problems:

- **Trains & track segments — Bluetooth.** Mobile units maintain a live Bluetooth link while moving. Dropouts are expected due to terrain and line-of-sight obstructions, so the system buffers the last known command/state and applies a dropout-tolerance window before flagging a fault.
- **Monorail barn (fixed nodes) — WiFi.** The barn's stationary sensor and motor nodes use WiFi, since Bluetooth range and pairing do not scale well across the barn's larger footprint.

The dual-radio split (Bluetooth for trains, WiFi for barn) is documented as a v1.1 item, with the hub daemon supporting both radios.

## Repository Structure

```
.
├── dashboard_v1.html            # v1 control dashboard (merged, functional)
├── sensor_system/               # Sensor framework and validation
├── Scripts/ and scripts/        # Automation and controller scripts
├── CAD-Models/                  # CAD sources
├── Configuration/               # Configuration files
├── Documentation/               # Detailed project documentation
├── Images/                      # System diagrams and renders
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Getting Started

**Requirements:** Python 3.12+, and Blender 3.4.1+ for CAD generation.

```bash
# Clone the repository
git clone https://github.com/lukew2580/WDW-Automated-Monorail-System.git
cd WDW-Automated-Monorail-System

# (Recommended) create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

For Raspberry Pi deployment, follow [`Documentation/RASPBERRY_PI_SETUP.md`](Documentation/RASPBERRY_PI_SETUP.md). For different deployment layouts, see [`SETUP_SCENARIOS.md`](SETUP_SCENARIOS.md).

## Dashboard

The v1 control dashboard is `dashboard_v1.html`. It provides live monitoring and control and talks to the automation API. Controls are functional when the API is running on the same machine as the browser.

## Documentation

Key references (full set under [`Documentation/`](Documentation/)):

- [`Documentation/API_DOCUMENTATION.md`](Documentation/API_DOCUMENTATION.md) — API reference
- [`Documentation/System_Architecture_Refinement.md`](Documentation/System_Architecture_Refinement.md) — architecture
- [`Documentation/RASPBERRY_PI_SETUP.md`](Documentation/RASPBERRY_PI_SETUP.md) — Pi setup
- [`Documentation/WDW_Monorail_Baseline_Sensor_Layout.md`](Documentation/WDW_Monorail_Baseline_Sensor_Layout.md) — sensor layout
- [`SENSOR_SPECIFICATIONS.md`](SENSOR_SPECIFICATIONS.md) — sensor specs
- [`HYBRID_MESHNET_VISION.md`](HYBRID_MESHNET_VISION.md) — mesh networking vision

## Contributing

Contributions are welcome. Please see [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) and the [`.github/CODE_OF_CONDUCT.md`](.github/CODE_OF_CONDUCT.md). Security policy: [`SECURITY.md`](SECURITY.md).

## License

Released under the MIT License. See [`LICENSE`](LICENSE) for details.
