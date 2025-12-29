#!/usr/bin/env python3
"""
Render the barn model with proper lighting and visibility
Run: blender -b CAD-Models/enhanced_barn_model.blend -P Scripts/render_barn_with_lighting.py
"""

import bpy
from mathutils import Vector

print("🔧 Setting up render...")

# Get scene and clear
scene = bpy.context.scene
world = scene.world

# Set background color
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.05, 0.05, 0.1, 1.0)  # Dark blue background

# Set up rendering
scene.render.engine = 'BLENDER_EEVEE'
scene.render.filepath = "/home/workspace/WDW-Automated-Monorail-System/CAD-Models/enhanced_barn_model.png"
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.samples = 128

print("💡 Adding lights...")

# Add key light
key_light = bpy.data.lights.new(name="KeyLight", type='SUN')
key_light.energy = 2.0
key_light_obj = bpy.data.objects.new(name="KeyLight", object_data=key_light)
scene.collection.objects.link(key_light_obj)
key_light_obj.location = (20, 15, 30)
key_light_obj.rotation_euler = (0.5, -0.5, 0)

# Add fill light
fill_light = bpy.data.lights.new(name="FillLight", type='SUN')
fill_light.energy = 0.8
fill_light_obj = bpy.data.objects.new(name="FillLight", object_data=fill_light)
scene.collection.objects.link(fill_light_obj)
fill_light_obj.location = (-15, -10, 20)
fill_light_obj.rotation_euler = (0.3, 2.5, 0)

# Add ambient light
ambient_light = bpy.data.lights.new(name="AmbientLight", type='SUN')
ambient_light.energy = 0.5
ambient_light_obj = bpy.data.objects.new(name="AmbientLight", object_data=ambient_light)
scene.collection.objects.link(ambient_light_obj)
ambient_light_obj.location = (0, 0, 50)

print("🎥 Setting up camera...")

# Find existing camera or create new one
camera = None
for obj in scene.objects:
    if obj.type == 'CAMERA':
        camera = obj
        break

if not camera:
    camera_data = bpy.data.cameras.new(name="Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    scene.collection.objects.link(camera)

# Position camera to show the barn nicely
camera.location = (30, -40, 25)
camera.rotation_euler = (1.1, 0, 0.7)
scene.camera = camera

print("🎨 Adjusting materials...")

# Make sure all objects are visible
for obj in scene.objects:
    if obj.type == 'MESH':
        obj.hide_render = False
        obj.hide_set(False)

# Set EEVEE-specific settings
eevee = scene.eevee
eevee.use_bloom = True
eevee.bloom_intensity = 0.1

print("🖼️  Rendering scene...")
print(f"   Resolution: 1920x1080")
print(f"   Samples: 128")
print(f"   Output: enhanced_barn_model.png")

bpy.ops.render.render(write_still=True)

print("✅ Render complete!")
print("📸 Image saved to: /home/workspace/WDW-Automated-Monorail-System/CAD-Models/enhanced_barn_model.png")

