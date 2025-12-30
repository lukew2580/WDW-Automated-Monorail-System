#!/usr/bin/env python3
"""
WDW Monorail Track System - CadQuery CAD Generation
Parametric modeling of the monorail track structure, supports, and switching systems.
"""

import cadquery as cq
from pathlib import Path


class MonorailTrackSystem:
    """Parametric monorail track system with CadQuery."""
    
    def __init__(self):
        # Track geometry
        self.track_width = 0.3  # 300mm wide track beam
        self.track_height = 0.5  # 500mm tall track profile
        self.track_thickness = 0.02  # 20mm steel plate
        
        # Support structure
        self.support_height = 8.0  # 8 meter tall support columns
        self.support_width = 0.6  # 600mm x 600mm columns
        self.beam_spacing = 30.0  # 30 meters between supports
        
        # Rail specifications
        self.rail_running_width = 0.25
        self.rail_guide_width = 0.15
        self.rail_thickness = 0.015
    
    def create_track_beam(self, length=30.0):
        """Create the main track beam with inverted-T cross-section."""
        # Top running surface
        top_plate = (
            cq.Workplane("XY")
            .box(length, self.track_width, self.track_thickness)
            .translate((0, 0, self.track_height / 2 - self.track_thickness / 2))
        )
        
        # Vertical beam web
        web = (
            cq.Workplane("XY")
            .box(length, self.track_thickness, self.track_height - self.track_thickness)
            .translate((0, 0, -self.track_thickness / 2))
        )
        
        # Guide rail (side)
        guide_rail = (
            cq.Workplane("XY")
            .box(length, self.rail_guide_width, self.track_height)
            .translate((self.track_width / 2 + self.rail_guide_width / 2, 0, 0))
        )
        
        track_beam = top_plate.union(web).union(guide_rail)
        return track_beam
    
    def create_support_column(self, height=8.0):
        """Create a support column structure."""
        # Main column
        main_column = (
            cq.Workplane("XY")
            .box(self.support_width, self.support_width, height)
        )
        
        # Internal reinforcement (ribs)
        rib_thickness = 0.02
        rib_height = height - 0.2
        
        rib_x = (
            cq.Workplane("XY")
            .box(self.support_width, rib_thickness, rib_height)
            .translate((0, 0, rib_height / 2))
        )
        
        rib_y = (
            cq.Workplane("XY")
            .box(rib_thickness, self.support_width, rib_height)
            .translate((0, 0, rib_height / 2))
        )
        
        column = main_column
        # Subtract internal cavity for weight reduction
        cavity = (
            cq.Workplane("XY")
            .box(self.support_width - 0.1, self.support_width - 0.1, height - 0.2)
            .translate((0, 0, (height - 0.2) / 2))
        )
        
        column = column.cut(cavity).union(rib_x).union(rib_y)
        return column
    
    def create_track_support_assembly(self, length=30.0):
        """Create full track section with support columns."""
        # Track beam
        track = self.create_track_beam(length)
        
        # Support columns at each end
        col_left = self.create_support_column(self.support_height).translate(
            (-length / 2, 0, -self.support_height / 2)
        )
        col_right = self.create_support_column(self.support_height).translate(
            (length / 2, 0, -self.support_height / 2)
        )
        
        # Mid-support column
        col_mid = self.create_support_column(self.support_height).translate(
            (0, 0, -self.support_height / 2)
        )
        
        assembly = track.union(col_left).union(col_right).union(col_mid)
        return assembly
    
    def create_switch_system(self):
        """Create monorail switch mechanism."""
        # Main track beam
        main_track = self.create_track_beam(15.0).translate((0, 0, 0))
        
        # Diverging track (angled switch)
        diverge_track = self.create_track_beam(15.0).rotate((0, 0, 0), (0, 0, 1), 8)
        diverge_track = diverge_track.translate((10, 3, 0))
        
        # Switch mechanism actuator housing
        actuator = (
            cq.Workplane("XY")
            .cylinder(0.5, 0.15)
            .translate((5, 0, 0))
        )
        
        assembly = main_track.union(diverge_track).union(actuator)
        return assembly
    
    def export_step(self, output_dir="/home/workspace/WDW-Automated-Monorail-System/CAD-Models"):
        """Export all components as STEP files."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track beam
        track = self.create_track_beam()
        track.val().exportStep(str(output_dir / "monorail_track_beam.step"))
        
        # Support column
        column = self.create_support_column()
        column.val().exportStep(str(output_dir / "monorail_support_column.step"))
        
        # Full assembly
        assembly = self.create_track_support_assembly()
        assembly.val().exportStep(str(output_dir / "monorail_track_assembly.step"))
        
        # Switch system
        switch = self.create_switch_system()
        switch.val().exportStep(str(output_dir / "monorail_switch_system.step"))
        
        print(f"✅ Exported track beam to: monorail_track_beam.step")
        print(f"✅ Exported support column to: monorail_support_column.step")
        print(f"✅ Exported track assembly to: monorail_track_assembly.step")
        print(f"✅ Exported switch system to: monorail_switch_system.step")


class SensorMount:
    """Parametric sensor mounting bracket."""
    
    def __init__(self):
        self.bracket_width = 0.1
        self.bracket_height = 0.15
        self.mount_diameter = 0.05
    
    def create_bracket(self):
        """Create sensor mounting bracket."""
        # Main bracket plate
        plate = (
            cq.Workplane("XY")
            .box(self.bracket_width, self.bracket_width, 0.01)
        )
        
        # Vertical post
        post = (
            cq.Workplane("XY")
            .box(0.01, 0.01, self.bracket_height)
            .translate((0, 0, self.bracket_height / 2 + 0.005))
        )
        
        # Mounting hole
        mount_hole = (
            cq.Workplane("XY")
            .cylinder(self.bracket_height, self.mount_diameter / 2)
            .translate((0, 0, self.bracket_height / 2))
        )
        
        bracket = plate.union(post).cut(mount_hole)
        return bracket
    
    def export_step(self, output_dir="/home/workspace/WDW-Automated-Monorail-System/CAD-Models"):
        """Export sensor mount."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        bracket = self.create_bracket()
        bracket.val().exportStep(str(output_dir / "sensor_mounting_bracket.step"))
        print(f"✅ Exported sensor mount to: sensor_mounting_bracket.step")


def main():
    """Generate all track system components."""
    print("🏗️  Generating WDW Monorail Track System CAD Models...")
    
    # Track system
    track_system = MonorailTrackSystem()
    track_system.export_step()
    
    # Sensor mounts
    sensor_mount = SensorMount()
    sensor_mount.export_step()
    
    print("\n✅ All CAD models generated successfully!")
    print("📁 Output location: /home/workspace/WDW-Automated-Monorail-System/CAD-Models/")


if __name__ == "__main__":
    main()

