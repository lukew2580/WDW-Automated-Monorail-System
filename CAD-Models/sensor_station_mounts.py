#!/usr/bin/env python3
import cadquery as cq
from pathlib import Path

print("🔧 Generating station sensor mounts...")

# Track sensor mount
mount = cq.Workplane("XY").box(40, 10, 10)
mount = mount.edges("|X").fillet(2)
mount = mount.faces(">Y").workplane().hole(3.5)
mount = mount.faces(">Y").workplane(centerOption="CenterOfMass").moveTo(15, 0).hole(3.5)

output = Path("/home/workspace/WDW-Automated-Monorail-System/CAD-Models")
cq.exporters.export(mount, str(output / "track_sensor_mount.step"))
print("✅ Track sensor mount bracket", output / "track_sensor_mount.step")

# BLE Repeater enclosure
repeater = cq.Workplane("XY").box(60, 45, 20)
repeater = repeater.edges("|Z").fillet(3)
cq.exporters.export(repeater, str(output / "ble_mesh_repeater.step"))
print("✅ BLE mesh repeater enclosure", output / "ble_mesh_repeater.step")

# Multi-sensor array housing
sensor1 = cq.Workplane("XY").box(25, 25, 20)

# Export
cq.exporters.export(sensor1, str(output / "monorail_sensor_housing.step"))
print("✅ Monorail sensor housing", output / "monorail_sensor_housing.step")

print(" ")
print("📁 All files generated successfully!")
