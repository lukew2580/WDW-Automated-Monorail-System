# WDW Monorail CAD - CadQuery Parametric Models

## 🎯 Overview

The monorail CAD system has been **converted from Blender binary files to CadQuery parametric Python models**. This provides better version control, reproducibility, and automation.

---

## 📦 What's Included

### Core Python Modules

#### 1. **Barn Structure** (`monorail_barn_cadquery.py`)
- Full maintenance facility modeling
- Parametric 70m × 50m × 8.5m structure
- 12 parking spaces with markings
- 4 maintenance bays with lift infrastructure
- Communication hub with antenna array
- HVAC system distribution (6 units)
- Electrical power distribution

**Generated Output**: `monorail_barn_cadquery.step` (635 KB)

#### 2. **Track System** (`monorail_track_system.py`)
- Inverted-T track beam profile
- Support column structures (hollow, reinforced)
- Track assembly with multiple supports
- Switch system with actuator housing
- Parametric sensor mounting brackets

**Generated Outputs**:
- `monorail_track_beam.step` (50 KB)
- `monorail_support_column.step` (101 KB)
- `monorail_track_assembly.step` (483 KB)
- `monorail_switch_system.step` (124 KB)
- `sensor_mounting_bracket.step` (37 KB)

---

## 🚀 Using the Models

### View in CAD Software
```bash
# Open in FreeCAD (free, open-source)
freecad monorail_barn_cadquery.step

# Or Fusion 360, Blender, etc. - all support STEP format
```

### Regenerate Models
```bash
# Run from CAD-Models directory
python3 monorail_barn_cadquery.py
python3 monorail_track_system.py
```

### Customize Dimensions
```python
from monorail_barn_cadquery import MonorailBarn

# Create custom barn
barn = MonorailBarn()
barn.length = 80.0  # Change to 80 meters
barn.width = 55.0   # Change to 55 meters
barn.export_step("./custom_barn.step")
```

### Export to Other Formats
```python
# Export to STL (3D printing)
barn.val().exportStl("output.stl")

# Export to DXF (2D CAD)
barn.val().exportDxf("output.dxf")
```

---

## 📊 File Sizes & Performance

| File | Size | Type | Use Case |
|------|------|------|----------|
| `monorail_barn_cadquery.py` | 8.4 KB | Source Code | Parametric generation |
| `monorail_barn_cadquery.step` | 635 KB | CAD (3D) | View/edit in CAD software |
| `monorail_track_system.py` | 7.4 KB | Source Code | Parametric generation |
| Track components (5 files) | 795 KB | CAD (3D) | Individual components |
| **Total Uncompressed** | ~1.4 MB | | Full CAD system |

### Comparison to Previous Blender Format
- **Before**: 9.1 MB (binary Blender + exports)
- **After**: 1.4 MB (Python source + STEP files)
- **Savings**: 7.7 MB (85% reduction!)
- **Git-friendly**: Python compresses better, easier diffs

---

## 🔧 Development & Customization

### Adding New Components

```python
from monorail_barn_cadquery import MonorailBarn
import cadquery as cq

class ExtendedBarn(MonorailBarn):
    def create_storage_area(self):
        """Add custom storage structure."""
        storage = (
            cq.Workplane("XY")
            .box(20, 15, 6)
            .translate((self.length/2 - 15, 0, 3))
        )
        return storage
    
    def create_complete_barn(self):
        """Override to include storage."""
        barn = super().create_complete_barn()
        storage = self.create_storage_area()
        return barn.union(storage)

# Generate custom barn
custom_barn = ExtendedBarn()
custom_barn.export_step("extended_barn.step")
```

### CadQuery Documentation
- [Official CadQuery Docs](https://cadquery.readthedocs.io/)
- [API Reference](https://cadquery.readthedocs.io/en/latest/classreference.html)
- [Examples & Tutorials](https://cadquery.readthedocs.io/en/latest/examples.html)

---

## 📋 Parametric Properties

### Barn Dimensions
```python
barn = MonorailBarn()

# Core structure
barn.length = 70.0  # meters (Y-axis)
barn.width = 50.0   # meters (X-axis)
barn.height = 8.5   # meters (Z-axis)
barn.wall_thickness = 0.3  # meters

# Parking
barn.parking_cols = 4  # columns
barn.parking_rows = 3  # rows
barn.parking_width = 12.5  # meters per space
barn.parking_length = 10.0  # meters per space

# Maintenance
barn.bay_width = 12.0  # meters
barn.bay_length = 15.0  # meters
barn.num_bays = 4  # number of bays
```

### Track System Dimensions
```python
track = MonorailTrackSystem()

# Track geometry
track.track_width = 0.3  # 300mm
track.track_height = 0.5  # 500mm
track.track_thickness = 0.02  # 20mm

# Supports
track.support_height = 8.0  # meters
track.support_width = 0.6  # 600mm × 600mm
track.beam_spacing = 30.0  # meters between supports
```

---

## ✅ Quality & Compatibility

### Software Support
- ✅ **FreeCAD** (free, open-source) - Full support
- ✅ **Blender** (free, open-source) - Import STEP files
- ✅ **Fusion 360** (free tier available) - Full support
- ✅ **SolidWorks** - Full STEP support
- ✅ **CAD software** - Any tool supporting STEP (ISO 10303-21)

### Export Formats
- **STEP** (.step) - Primary CAD format ✅
- **STL** (.stl) - 3D printing format
- **DXF** (.dxf) - 2D drawings
- **SVG** (.svg) - 2D vector

### Precision
- **Python source**: Exact parametric dimensions
- **STEP export**: Full CAD precision (ISO standard)
- **Suitable for**: Engineering, 3D printing, visualization

---

## 📚 Migration Notes

### What Changed
- ✅ Converted from Blender binary to Python parametric source
- ✅ Removed large binary files from Git (better version control)
- ✅ Created dedicated CadQuery modules
- ✅ Generated STEP files for CAD software compatibility
- ✅ Backed up original files to `.cad_backup/`

### Backward Compatibility
- Original `.blend` files backed up in `.cad_backup/`
- All models regenerable from Python source
- STEP format universally supported

### For Version Control
- Python files: Excellent for Git (text-based, compressible)
- STEP files: Can be re-generated, don't need to commit to Git
- Consider: Add STEP files to `.gitignore` if regenerating frequently

---

## 🔄 Workflow

### Standard Workflow
1. **Edit dimensions** in Python file
2. **Run generator**: `python3 monorail_barn_cadquery.py`
3. **View output**: Open `.step` file in CAD software
4. **Commit changes**: `git commit CAD-Models/*.py`

### Collaboration Workflow
1. Engineer A modifies dimensions in Python
2. Commits to Git: `git push`
3. Engineer B pulls: `git pull`
4. Regenerates models: `python3 monorail_barn_cadquery.py`
5. Reviews in CAD software
6. Approves changes

---

## 💡 Tips & Tricks

### Generate Multiple Variants
```python
# Create a script to generate multiple variants
for length in [60, 70, 80, 90]:
    for width in [40, 50, 60]:
        barn = MonorailBarn()
        barn.length = length
        barn.width = width
        barn.export_step(f"barn_{length}x{width}.step")
```

### Extract Component Data
```python
barn = MonorailBarn()

# Get all component volumes (useful for material calculations)
components = [
    barn.create_floor(),
    barn.create_walls(),
    barn.create_roof(),
]

for comp in components:
    volume = comp.val().Volume
    print(f"Component volume: {volume:.2f} m³")
```

### Batch Export
```python
track = MonorailTrackSystem()

# Export all components at once
track.export_step()  # Exports 5 STEP files

# Then convert to other formats
import subprocess
subprocess.run(["freecad", "-b", "convert_to_stl.macro"])
```

---

## 🎓 Learning Resources

### CadQuery
- [CadQuery GitHub](https://github.com/CadQuery/cadquery)
- [Getting Started](https://cadquery.readthedocs.io/en/latest/quickstart.html)
- [Community Examples](https://github.com/CadQuery/cadquery/wiki/Gallery)

### 3D CAD & Engineering
- [FreeCAD Documentation](https://wiki.freecadweb.org/)
- [STEP Format (ISO 10303)](https://en.wikipedia.org/wiki/STEP_file)
- [3D Modeling Best Practices](https://www.autodesk.com/products/fusion/blog)

---

## ❓ FAQ

**Q: Can I still use the old Blender files?**  
A: Yes! They're backed up in `.cad_backup/`. But the Python source is the canonical version now.

**Q: How do I modify the models?**  
A: Edit the Python files directly - change dimensions and re-run the script.

**Q: What if I need Blender format?**  
A: Open the STEP file in Blender and export as `.blend` if needed.

**Q: Can I share these models with collaborators?**  
A: Yes! Share the Python files (small, text-based) or STEP files (universal format).

**Q: What's the best CAD software to view these?**  
A: FreeCAD (free) is perfect. Fusion 360 (free tier) is also excellent.

---

## 📞 Support

- **Issue**: Models not generating? Check CadQuery installation: `pip install cadquery`
- **Customization**: Edit Python files and re-run generators
- **Collaboration**: Commit Python source to Git for easy merging
- **Legacy**: Original files available in `.cad_backup/` directory

---

## 🚀 Next Steps

1. **Open** a STEP file in your CAD software
2. **Review** the model geometry
3. **Modify** dimensions in Python if needed
4. **Share** with team (Python files for editing, STEP for viewing)
5. **Integrate** into broader WDW monorail system

---

**Status**: ✅ Ready for Production  
**Format**: CadQuery Parametric Python  
**Version**: 1.0  
**Last Updated**: December 30, 2025

