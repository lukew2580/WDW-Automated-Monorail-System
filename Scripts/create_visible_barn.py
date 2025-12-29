#!/usr/bin/env python3
"""
Create a visible, simple monorail barn model with proper rendering
"""

import bpy
import bmesh
from mathutils import Vector

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("🏗️ Building barn structure...")

# Function to add a box
def create_box(name, location, scale, color):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.location = location
    obj.scale = scale
    
    # Create material
    mat = bpy.data.materials.new(name=f"{name}_mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (*color, 1.0)
    bsdf.inputs[9].default_value = 0.3  # roughness
    
    obj.data.materials.append(mat)
    return obj

# Create main barn structure
print("   Creating walls...")
create_box("Main_Barn", (0, 0, 4), (30, 40, 8), (0.7, 0.65, 0.5))  # Main structure
create_box("Roof", (0, 0, 10), (32, 42, 1), (0.6, 0.3, 0.2))  # Roof

print("   Creating parking area...")
create_box("Parking_Floor", (0, -25, 0.1), (30, 15, 0.2), (0.3, 0.3, 0.35))

print("   Creating maintenance bays...")
for i in range(4):
    x = -10 + (i * 6)
    create_box(f"Bay_{i}", (x, 5, 3), (5, 8, 6), (0.8, 0.8, 0.8))

print("   Creating charging stations...")
for i in range(4):
    y = -15 + (i * 8)
    create_box(f"Charger_{i}", (-12, y, 1), (2, 3, 2), (0.2, 0.6, 0.8))

print("   Creating support pillars...")
positions = [(-12, -15), (-12, 15), (12, -15), (12, 15), (0, 0)]
for i, (x, y) in enumerate(positions):
    create_box(f"Pillar_{i}", (x, y, 2), (1, 1, 4), (0.5, 0.5, 0.5))

# Set up scene
scene = bpy.context.scene
world = scene.world

print("🎨 Setting up materials and lighting...")

# World background
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.1, 0.1, 0.15, 1.0)

# Render settings
scene.render.engine = 'BLENDER_EEVEE'
scene.render.filepath = "/home/workspace/WDW-Automated-Monorail-System/CAD-Models/enhanced_barn_model.png"
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Add lights
print("💡 Adding illumination...")

# Key light - bright sun
key_light = bpy.data.lights.new(name="Sun", type='SUN')
key_light.energy = 3.0
key_light_obj = bpy.data.objects.new(name="Sun", object_data=key_light)
scene.collection.objects.link(key_light_obj)
key_light_obj.location = (30, 30, 40)
key_light_obj.rotation_euler = (0.4, 0.3, 0)

# Fill light
fill_light = bpy.data.lights.new(name="Fill", type='SUN')
fill_light.energy = 1.2
fill_light_obj = bpy.data.objects.new(name="Fill", object_data=fill_light)
scene.collection.objects.link(fill_light_obj)
fill_light_obj.location = (-20, -20, 25)
fill_light_obj.rotation_euler = (0.5, -2.5, 0)

# Back light for separation
back_light = bpy.data.lights.new(name="Back", type='SUN')
back_light.energy = 0.8
back_light_obj = bpy.data.objects.new(name="Back", object_data=back_light)
scene.collection.objects.link(back_light_obj)
back_light_obj.location = (0, -50, 20)

print("📷 Setting up camera...")

# Create camera
camera_data = bpy.data.cameras.new(name="Camera")
camera = bpy.data.objects.new("Camera", camera_data)
scene.collection.objects.link(camera)
camera.location = (45, -55, 30)
camera.rotation_euler = (1.2, 0, 0.8)
scene.camera = camera

# Set EEVEE settings
eevee = scene.eevee
eevee.taa_render_samples = 64
eevee.use_bloom = True
eevee.bloom_intensity = 0.2
eevee.use_gtao = True
eevee.gtao_distance = 0.5

print("🖼️  Rendering...")

# Make sure everything is visible
for obj in scene.objects:
    obj.hide_set(False)
    obj.hide_render = False

# Render
bpy.ops.render.render(write_still=True)

print("✅ Complete!")
print("📸 Saved: /home/workspace/WDW-Automated-Monorail-System/CAD-Models/enhanced_barn_model.png")

# Save the blend file
bpy.ops.wm.save_as_mainfile(filepath="/home/workspace/WDW-Automated-Monorail-System/CAD-Models/enhanced_barn_model.blend")
print("💾 Saved: enhanced_barn_model.blend")


