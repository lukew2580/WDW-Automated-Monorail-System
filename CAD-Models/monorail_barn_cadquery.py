#!/usr/bin/env python3
"""
WDW Monorail Barn - CadQuery CAD Generation
Parametric model of the maintenance facility with parking, bays, and infrastructure.
"""

import cadquery as cq
from pathlib import Path


class MonorailBarn:
    """Parametric barn structure using CadQuery."""
    
    def __init__(self):
        # Overall dimensions
        self.length = 70.0  # meters
        self.width = 50.0   # meters
        self.height = 8.5   # meters
        self.wall_thickness = 0.3  # meters
        
        # Parking grid
        self.parking_cols = 4
        self.parking_rows = 3
        self.parking_width = self.width / self.parking_cols
        self.parking_length = 10.0
        
        # Maintenance bays
        self.bay_width = 12.0
        self.bay_length = 15.0
        self.num_bays = 4
    
    def create_floor(self):
        """Create concrete floor slab."""
        floor = (
            cq.Workplane("XY")
            .box(self.length, self.width, 0.4)
            .translate((0, 0, -0.2))
        )
        return floor
    
    def create_walls(self):
        """Create building walls."""
        # Outer perimeter
        outer_box = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height)
        )
        
        # Inner cavity
        inner_box = (
            cq.Workplane("XY")
            .box(self.length - self.wall_thickness * 2,
                 self.width - self.wall_thickness * 2,
                 self.height)
            .translate((0, 0, 0))
        )
        
        walls = outer_box.cut(inner_box)
        
        # Add door opening (12m x 8m)
        door_opening = (
            cq.Workplane("XY")
            .box(12, 8, 3)
            .translate((0, -self.width / 2 + self.wall_thickness / 2, 1.5))
        )
        walls = walls.cut(door_opening)
        
        return walls
    
    def create_roof(self):
        """Create roof structure."""
        # Flat roof with slope
        roof = (
            cq.Workplane("XY")
            .box(self.length, self.width, 0.3)
            .translate((0, 0, self.height - 0.15))
        )
        
        # Roof trusses (simplified)
        num_trusses = 5
        spacing = self.length / (num_trusses - 1)
        
        for i in range(num_trusses):
            x = -self.length / 2 + i * spacing
            truss = (
                cq.Workplane("XY")
                .box(0.3, self.width, 0.5)
                .translate((x, 0, self.height - 0.4))
            )
            roof = roof.union(truss)
        
        return roof
    
    def create_structural_columns(self):
        """Create support columns."""
        col_width = 2.0
        col_height = self.height
        
        # Create 6 columns in grid pattern
        columns = None
        positions = [
            (-self.length / 3, -self.width / 3),
            (-self.length / 3, self.width / 3),
            (0, -self.width / 3),
            (0, self.width / 3),
            (self.length / 3, -self.width / 3),
            (self.length / 3, self.width / 3),
        ]
        
        for x, y in positions:
            col = (
                cq.Workplane("XY")
                .box(col_width, col_width, col_height)
                .translate((x, y, col_height / 2))
            )
            columns = col if columns is None else columns.union(col)
        
        return columns
    
    def create_parking_spaces(self):
        """Create parking slot markings and infrastructure."""
        spaces = None
        
        for row in range(self.parking_rows):
            for col in range(self.parking_cols):
                # Calculate position
                x = -self.length / 2 + self.parking_length / 2 + row * self.parking_length
                y = -self.width / 2 + self.parking_width / 2 + col * self.parking_width
                
                # Create parking space outline (yellow lines)
                outline = (
                    cq.Workplane("XY")
                    .box(self.parking_length, self.parking_width, 0.01)
                    .translate((x, y, 0.01))
                )
                
                spaces = outline if spaces is None else spaces.union(outline)
        
        return spaces
    
    def create_maintenance_bays(self):
        """Create maintenance bay infrastructure."""
        bays = None
        bay_spacing = (self.width - self.bay_width * self.num_bays) / (self.num_bays + 1)
        
        for i in range(self.num_bays):
            # Bay position
            y = -self.width / 2 + bay_spacing + i * (self.bay_width + bay_spacing)
            x = self.length / 2 - self.bay_length / 2
            
            # Bay floor (epoxy coating)
            bay_floor = (
                cq.Workplane("XY")
                .box(self.bay_length, self.bay_width, 0.05)
                .translate((x, y, 0.025))
            )
            
            # Vehicle lift
            lift = (
                cq.Workplane("XY")
                .box(2, 2, 0.5)
                .translate((x - 3, y, 0.25))
            )
            
            bay = bay_floor.union(lift)
            bays = bay if bays is None else bays.union(bay)
        
        return bays
    
    def create_communication_hub(self):
        """Create central communication hub with antenna array."""
        # Hub base
        hub = (
            cq.Workplane("XY")
            .box(4, 4, 3)
            .translate((0, 0, 1.5))
        )
        
        # Antenna mast
        mast = (
            cq.Workplane("XY")
            .cylinder(6, 0.2)
            .translate((0, 0, 3 + 3))
        )
        
        # Antennas
        antenna1 = (
            cq.Workplane("XY")
            .cylinder(0.5, 0.05)
            .rotate((0, 0, 0), (1, 0, 0), 45)
            .translate((0, 0, 8))
        )
        
        assembly = hub.union(mast).union(antenna1)
        return assembly
    
    def create_hvac_system(self):
        """Create HVAC distribution units."""
        hvac_units = None
        num_units = 6
        spacing = self.length / (num_units + 1)
        
        for i in range(num_units):
            x = -self.length / 2 + spacing * (i + 1)
            
            # Ceiling unit
            unit = (
                cq.Workplane("XY")
                .box(1.5, 1.5, 0.5)
                .translate((x, 0, self.height - 0.25))
            )
            
            hvac_units = unit if hvac_units is None else hvac_units.union(unit)
        
        return hvac_units
    
    def create_power_distribution(self):
        """Create electrical distribution infrastructure."""
        # Main panel
        panel = (
            cq.Workplane("XY")
            .box(1, 2, 3)
            .translate((self.length / 2 - 1.5, self.width / 2 - 2, 1.5))
        )
        
        # Conduit runs
        conduit = (
            cq.Workplane("XY")
            .cylinder(self.length / 2, 0.1)
            .rotate((0, 0, 0), (0, 1, 0), 90)
            .translate((0, self.width / 2 - 0.3, self.height - 0.5))
        )
        
        return panel.union(conduit)
    
    def create_complete_barn(self):
        """Assemble complete barn structure."""
        # Core structure
        floor = self.create_floor()
        walls = self.create_walls()
        roof = self.create_roof()
        columns = self.create_structural_columns()
        
        # Systems
        parking = self.create_parking_spaces()
        bays = self.create_maintenance_bays()
        hub = self.create_communication_hub()
        hvac = self.create_hvac_system()
        power = self.create_power_distribution()
        
        # Assemble
        barn = floor.union(walls).union(roof).union(columns)
        barn = barn.union(parking).union(bays).union(hub)
        barn = barn.union(hvac).union(power)
        
        return barn
    
    def export_step(self, output_dir="/home/workspace/WDW-Automated-Monorail-System/CAD-Models"):
        """Export barn structure."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("🏗️  Building barn structure...")
        barn = self.create_complete_barn()
        
        output_path = output_dir / "monorail_barn_cadquery.step"
        barn.val().exportStep(str(output_path))
        print(f"✅ Exported barn structure to: monorail_barn_cadquery.step")


def main():
    """Generate barn CAD model."""
    barn = MonorailBarn()
    barn.export_step()
    print("✅ Barn CAD model generation complete!")


if __name__ == "__main__":
    main()

