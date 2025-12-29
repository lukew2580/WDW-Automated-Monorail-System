#!/usr/bin/env python3
"""
Enhanced Monorail Barn CAD Model Generator
Creates a detailed 3D model of the WDW monorail barn with parking, maintenance areas,
sensor infrastructure, and support systems.
"""

import bpy
import bmesh
import json
import os
from mathutils import Vector, Matrix
from datetime import datetime

class MonorailBarnGenerator:
    def __init__(self):
        self.barn_data = {
            "name": "Enhanced Monorail Barn",
            "version": "2.0",
            "created": datetime.now().isoformat(),
            "components": [],
            "sensors": []
        }
        self.parking_slots = 12
        self.maintenance_bays = 4
        self.materials = {}
        
    def clear_scene(self):
        """Clear all objects from the current Blender scene."""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
    def create_material(self, name, color, roughness=0.5, metallic=0.0):
        """Create a material with given properties."""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        self.materials[name] = mat
        return mat
    
    def create_floor(self):
        """Create the barn floor."""
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.1))
        floor = bpy.context.active_object
        floor.scale = (35, 25, 0.2)
        floor.name = "Floor"
        
        # Apply concrete material
        concrete_mat = self.create_material("Concrete", (0.4, 0.4, 0.4), roughness=0.7)
        floor.data.materials.append(concrete_mat)
        
        self.barn_data["components"].append({
            "name": "Floor",
            "type": "structural",
            "dimensions": (70, 50, 0.4),
            "location": (0, 0, -0.1)
        })
        return floor
    
    def create_support_beams(self):
        """Create the main support beam structure."""
        beams = []
        beam_spacing_x = 14  # Space between beams along length
        beam_spacing_y = 12  # Space between beams along width
        beam_height = 8
        
        steel_mat = self.create_material("Steel", (0.3, 0.3, 0.35), roughness=0.3, metallic=0.8)
        
        # Main beams along length
        for x in [-14, 0, 14]:
            for y in [-8, 8]:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, beam_height/2))
                beam = bpy.context.active_object
                beam.scale = (1, 1, beam_height)
                beam.name = f"Support_Beam_{x}_{y}"
                beam.data.materials.append(steel_mat)
                beams.append(beam)
                
                self.barn_data["components"].append({
                    "name": f"Support_Beam_{x}_{y}",
                    "type": "beam",
                    "dimensions": (2, 2, beam_height*2),
                    "location": (x, y, beam_height/2)
                })
        
        # Roof beams
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, beam_height))
        roof_beam = bpy.context.active_object
        roof_beam.scale = (35, 25, 0.5)
        roof_beam.name = "Roof_Beam"
        roof_beam.data.materials.append(steel_mat)
        beams.append(roof_beam)
        
        self.barn_data["components"].append({
            "name": "Roof_Beam",
            "type": "structural",
            "dimensions": (70, 50, 1),
            "location": (0, 0, beam_height)
        })
        
        return beams
    
    def create_roof(self):
        """Create the barn roof."""
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 8.4))
        roof = bpy.context.active_object
        roof.scale = (35.5, 25.5, 0.3)
        roof.name = "Roof"
        
        roof_mat = self.create_material("Corrugated Metal", (0.5, 0.5, 0.5), roughness=0.4, metallic=0.9)
        roof.data.materials.append(roof_mat)
        
        self.barn_data["components"].append({
            "name": "Roof",
            "type": "roofing",
            "dimensions": (71, 51, 0.6),
            "location": (0, 0, 8.4)
        })
        return roof
    
    def create_walls(self):
        """Create barn walls."""
        walls = []
        wall_mat = self.create_material("Brick", (0.6, 0.4, 0.3), roughness=0.8)
        
        # Front and back walls
        for y in [-12.5, 12.5]:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, y, 4))
            wall = bpy.context.active_object
            wall.scale = (35.5, 0.3, 8)
            wall.name = f"Wall_{'Front' if y < 0 else 'Back'}"
            wall.data.materials.append(wall_mat)
            walls.append(wall)
        
        # Side walls
        for x in [-35, 35]:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 4))
            wall = bpy.context.active_object
            wall.scale = (0.3, 25.5, 8)
            wall.name = f"Wall_{'Left' if x < 0 else 'Right'}"
            wall.data.materials.append(wall_mat)
            walls.append(wall)
        
        self.barn_data["components"].append({
            "name": "Walls",
            "type": "structural",
            "count": 4,
            "dimensions": (35.5, 25.5, 8)
        })
        
        return walls
    
    def create_parking_slots(self):
        """Create 12 monorail parking slots."""
        slots = []
        slot_mat = self.create_material("Parking_Floor", (0.2, 0.2, 0.2), roughness=0.9)
        line_mat = self.create_material("Yellow_Line", (1.0, 1.0, 0.0), roughness=0.6)
        
        # Arrange in 3 rows of 4 slots
        spacing_x = 12
        spacing_y = 10
        start_x = -18
        start_y = -15
        
        for row in range(3):
            for col in range(4):
                x = start_x + (row * spacing_x)
                y = start_y + (col * spacing_y)
                z = 0.1
                
                # Parking slot floor
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, z))
                slot = bpy.context.active_object
                slot.scale = (5, 8, 0.1)
                slot.name = f"Parking_Slot_{row}_{col}"
                slot.data.materials.append(slot_mat)
                slots.append(slot)
                
                # Parking lines (simple representation)
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x - 2.3, y - 3.5, 0.11))
                line = bpy.context.active_object
                line.scale = (0.1, 8, 0.01)
                line.name = f"Slot_Line_Left_{row}_{col}"
                line.data.materials.append(line_mat)
                
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 2.3, y - 3.5, 0.11))
                line = bpy.context.active_object
                line.scale = (0.1, 8, 0.01)
                line.name = f"Slot_Line_Right_{row}_{col}"
                line.data.materials.append(line_mat)
                
                self.barn_data["components"].append({
                    "name": f"Parking_Slot_{row}_{col}",
                    "type": "parking",
                    "slot_number": row * 4 + col + 1,
                    "dimensions": (10, 16, 0.2),
                    "location": (x, y, z),
                    "capacity": 1
                })
        
        return slots
    
    def create_maintenance_bays(self):
        """Create maintenance bays for vehicle service."""
        bays = []
        bay_mat = self.create_material("Maintenance_Bay", (0.35, 0.35, 0.35), roughness=0.6)
        
        bay_positions = [
            (-28, -20),
            (-28, 0),
            (-28, 20),
            (-8, -20)
        ]
        
        for idx, (x, y) in enumerate(bay_positions):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.15))
            bay = bpy.context.active_object
            bay.scale = (6, 12, 0.15)
            bay.name = f"Maintenance_Bay_{idx + 1}"
            bay.data.materials.append(bay_mat)
            bays.append(bay)
            
            # Create equipment racks in bays
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 2, y, 2))
            rack = bpy.context.active_object
            rack.scale = (1, 2, 4)
            rack.name = f"Equipment_Rack_{idx + 1}"
            rack.data.materials.append(self.materials.get("Steel", self.create_material("Steel_Bay", (0.3, 0.3, 0.35))))
            
            self.barn_data["components"].append({
                "name": f"Maintenance_Bay_{idx + 1}",
                "type": "maintenance",
                "dimensions": (12, 24, 0.3),
                "location": (x, y, 0.15),
                "equipment": ["vehicle lift", "diagnostic station", "hydraulics"]
            })
        
        return bays
    
    def create_consolidation_zone(self):
        """Create central consolidation zone."""
        bpy.ops.mesh.primitive_cube_add(size=1, location=(15, 0, 0.2))
        zone = bpy.context.active_object
        zone.scale = (8, 10, 0.2)
        zone.name = "Consolidation_Zone"
        
        consol_mat = self.create_material("Consolidation_Floor", (0.25, 0.4, 0.6), roughness=0.7)
        zone.data.materials.append(consol_mat)
        
        self.barn_data["components"].append({
            "name": "Consolidation_Zone",
            "type": "operational",
            "dimensions": (16, 20, 0.4),
            "location": (15, 0, 0.2),
            "purpose": "Vehicle consolidation and load balancing"
        })
        
        return zone
    
    def create_communication_hub(self):
        """Create central communication hub."""
        bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=3, location=(20, 0, 1.5))
        hub = bpy.context.active_object
        hub.name = "Communication_Hub"
        
        hub_mat = self.create_material("Hub_Metal", (0.25, 0.25, 0.3), roughness=0.2, metallic=1.0)
        hub.data.materials.append(hub_mat)
        
        # Antenna array
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.1, 
                depth=2,
                location=(20 + 1.8 * math.cos(rad), 0 + 1.8 * math.sin(rad), 3)
            )
            antenna = bpy.context.active_object
            antenna.name = f"Antenna_{angle}"
            antenna.data.materials.append(hub_mat)
        
        self.barn_data["components"].append({
            "name": "Communication_Hub",
            "type": "infrastructure",
            "dimensions": (3, 3, 3),
            "location": (20, 0, 1.5),
            "capabilities": ["WiFi 6E", "Bluetooth 5.3", "Mesh networking", "4G backup"]
        })
        
        return hub
    
    def create_sensors(self):
        """Create sensor network infrastructure."""
        sensors = []
        sensor_mat = self.create_material("Sensor_Red", (1.0, 0.0, 0.0), roughness=0.3)
        
        # Entry/exit sensors
        sensor_positions = [
            (-34, 0, 5, "Entry_Gate_Sensor"),
            (34, 0, 5, "Exit_Gate_Sensor"),
            (0, -12, 5, "Front_Monitor"),
            (0, 12, 5, "Rear_Monitor"),
            (20, 0, 3, "Hub_Security_Sensor"),
        ]
        
        # Parking slot sensors
        for row in range(3):
            for col in range(4):
                x = -18 + (row * 12)
                y = -15 + (col * 10)
                sensor_positions.append((x, y, 1.5, f"Parking_Sensor_{row}_{col}"))
        
        for x, y, z, name in sensor_positions:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(x, y, z))
            sensor = bpy.context.active_object
            sensor.name = name
            sensor.data.materials.append(sensor_mat)
            sensors.append(sensor)
            
            self.barn_data["sensors"].append({
                "name": name,
                "type": "occupancy" if "Parking" in name else "access",
                "location": (x, y, z),
                "range": 50
            })
        
        return sensors
    
    def create_climate_system(self):
        """Create HVAC and climate control infrastructure."""
        hvac = []
        hvac_mat = self.create_material("HVAC_Unit", (0.4, 0.4, 0.4), roughness=0.5)
        
        # Ceiling-mounted HVAC units
        for x in [-20, 0, 20]:
            for y in [-10, 10]:
                bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 7.8))
                unit = bpy.context.active_object
                unit.scale = (2, 2, 0.5)
                unit.name = f"HVAC_Unit_{x}_{y}"
                unit.data.materials.append(hvac_mat)
                hvac.append(unit)
        
        self.barn_data["components"].append({
            "name": "HVAC_System",
            "type": "infrastructure",
            "units": 6,
            "coverage": "full barn"
        })
        
        return hvac
    
    def create_lighting_system(self):
        """Create lighting infrastructure."""
        lights_data = []
        light_positions = [
            (-25, -15, 7.5),
            (-25, 0, 7.5),
            (-25, 15, 7.5),
            (0, -15, 7.5),
            (0, 0, 7.5),
            (0, 15, 7.5),
            (25, -15, 7.5),
            (25, 0, 7.5),
            (25, 15, 7.5),
        ]
        
        for x, y, z in light_positions:
            light = bpy.data.lights.new(name=f"Light_{x}_{y}", type='AREA')
            light.energy = 500
            light.size = 4
            
            light_obj = bpy.data.objects.new(name=f"Light_{x}_{y}", object_data=light)
            bpy.context.collection.objects.link(light_obj)
            light_obj.location = (x, y, z)
            lights_data.append(light_obj)
        
        self.barn_data["components"].append({
            "name": "Lighting_System",
            "type": "infrastructure",
            "units": 9,
            "type_led": "Full spectrum LED",
            "color_temperature": "5000K"
        })
        
        return lights_data
    
    def create_power_distribution(self):
        """Create power distribution infrastructure."""
        power = []
        power_mat = self.create_material("Conduit", (0.1, 0.1, 0.1), roughness=0.8)
        
        # Main power conduit along walls
        for x in [-34, 34]:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=50, location=(x, 0, 2))
            conduit = bpy.context.active_object
            conduit.rotation_euler = (0, 1.5708, 0)  # Rotate 90 degrees
            conduit.name = f"Main_Conduit_{'Left' if x < 0 else 'Right'}"
            conduit.data.materials.append(power_mat)
            power.append(conduit)
        
        # Charging stations for vehicles
        for i in range(4):
            x = -25 + (i * 15)
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 20, 1))
            charger = bpy.context.active_object
            charger.scale = (1, 0.5, 1.5)
            charger.name = f"Charging_Station_{i+1}"
            charger.data.materials.append(power_mat)
            power.append(charger)
        
        self.barn_data["components"].append({
            "name": "Power_Distribution",
            "type": "infrastructure",
            "capacity": "480V, 3-phase",
            "charging_stations": 4,
            "backup_generator": "500kW diesel"
        })
        
        return power
    
    def save_barn_data(self, filepath):
        """Save barn metadata to JSON."""
        with open(filepath, 'w') as f:
            json.dump(self.barn_data, f, indent=2)
    
    def generate_full_barn(self, output_file):
        """Generate the complete barn model."""
        print("🏗️  Generating enhanced monorail barn...")
        
        # Clear existing scene
        self.clear_scene()
        
        # Set up materials
        print("📦 Creating materials...")
        self.create_material("Concrete", (0.4, 0.4, 0.4))
        
        # Build barn structure
        print("🏭 Building barn structure...")
        self.create_floor()
        self.create_support_beams()
        self.create_roof()
        self.create_walls()
        
        print("🅿️  Creating parking infrastructure...")
        self.create_parking_slots()
        
        print("🔧 Creating maintenance facilities...")
        self.create_maintenance_bays()
        
        print("🔄 Creating operational zones...")
        self.create_consolidation_zone()
        
        print("📡 Creating communication hub...")
        self.create_communication_hub()
        
        print("📊 Installing sensor network...")
        self.create_sensors()
        
        print("❄️  Installing climate control...")
        self.create_climate_system()
        
        print("💡 Installing lighting system...")
        self.create_lighting_system()
        
        print("🔌 Installing power distribution...")
        self.create_power_distribution()
        
        # Set up scene for rendering
        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_EEVEE'
        scene.render.image_settings.file_format = 'PNG'
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.resolution_percentage = 100
        
        # Set camera
        bpy.ops.object.camera_add(location=(40, 40, 25))
        camera = bpy.context.active_object
        camera.name = "Camera"
        camera.rotation_euler = (1.1, 0, 0.785)
        scene.camera = camera
        
        # Save blend file
        print(f"💾 Saving blend file: {output_file}")
        bpy.ops.wm.save_as_mainfile(filepath=output_file)
        
        # Save metadata
        json_file = output_file.replace('.blend', '_metadata.json')
        print(f"📝 Saving metadata: {json_file}")
        self.save_barn_data(json_file)
        
        print(f"✅ Enhanced barn model created successfully!")
        print(f"📊 Total components: {len(self.barn_data['components'])}")
        print(f"📡 Total sensors: {len(self.barn_data['sensors'])}")

if __name__ == "__main__":
    # This script is designed to run within Blender
    # Usage: blender -b -P create_enhanced_barn_model.py
    generator = MonorailBarnGenerator()
    output_path = "/home/workspace/WDW-Automated-Monorail-System/CAD-Models/enhanced_barn_model.blend"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    generator.generate_full_barn(output_path)


