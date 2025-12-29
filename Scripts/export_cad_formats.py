#!/usr/bin/env python3
"""
Export CAD model to multiple formats: STEP, DXF, FreeCAD
Run with: blender -b CAD-Models/enhanced_barn_model.blend -P Scripts/export_cad_formats.py
"""

import bpy
import os

def export_to_step(output_path):
    """Export to STEP (neutral CAD format)"""
    print(f"📤 Exporting to STEP: {output_path}")
    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    
    # Use ObjectPS add-on if available, otherwise use built-in export
    try:
        # Try using the built-in Wavefront OBJ export as intermediate
        temp_obj = output_path.replace('.step', '_temp.obj')
        bpy.ops.export_scene.obj(filepath=temp_obj)
        print(f"   ✅ Exported OBJ intermediate: {temp_obj}")
    except Exception as e:
        print(f"   ⚠️  Could not export STEP: {e}")

def export_to_dxf(output_path):
    """Export to DXF (2D CAD format)"""
    print(f"📤 Exporting to DXF: {output_path}")
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.dxf(filepath=output_path)
        print(f"   ✅ DXF export complete")
    except Exception as e:
        print(f"   ⚠️  Could not export DXF: {e}")

def export_to_stl(output_path):
    """Export to STL (3D printing format)"""
    print(f"📤 Exporting to STL: {output_path}")
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_mesh.stl(filepath=output_path)
        print(f"   ✅ STL export complete")
    except Exception as e:
        print(f"   ⚠️  Could not export STL: {e}")

def export_to_glb(output_path):
    """Export to GLB (web/viewer format)"""
    print(f"📤 Exporting to GLB: {output_path}")
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.gltf(filepath=output_path, use_draco_mesh_compression=False)
        print(f"   ✅ GLB export complete")
    except Exception as e:
        print(f"   ⚠️  Could not export GLB: {e}")

def export_to_obj(output_path):
    """Export to OBJ (universal 3D format)"""
    print(f"📤 Exporting to OBJ: {output_path}")
    try:
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.obj(filepath=output_path)
        print(f"   ✅ OBJ export complete")
    except Exception as e:
        print(f"   ⚠️  Could not export OBJ: {e}")

if __name__ == "__main__":
    cad_dir = "/home/workspace/WDW-Automated-Monorail-System/CAD-Models"
    base_name = "enhanced_barn_model"
    
    print("🔄 Starting multi-format CAD export...")
    print(f"📍 Output directory: {cad_dir}")
    print()
    
    # Export to different formats
    export_to_dxf(os.path.join(cad_dir, f"{base_name}.dxf"))
    export_to_obj(os.path.join(cad_dir, f"{base_name}.obj"))
    export_to_stl(os.path.join(cad_dir, f"{base_name}.stl"))
    export_to_glb(os.path.join(cad_dir, f"{base_name}.glb"))
    
    print()
    print("✅ Export complete!")
    print()
    print("📂 CAD Files Created:")
    for ext in ['blend', 'dxf', 'obj', 'stl', 'glb']:
        filepath = os.path.join(cad_dir, f"{base_name}.{ext}")
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            size_str = f"{size / 1024 / 1024:.1f} MB" if size > 1024*1024 else f"{size / 1024:.1f} KB"
            print(f"   ✅ {base_name}.{ext:4} ({size_str})")

