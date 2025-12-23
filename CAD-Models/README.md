# WDW Automated Monorail System - CAD Models

This directory contains Computer-Aided Design (CAD) models for the Walt Disney World Automated Monorail System. These models represent the physical components, sensor placements, and system architecture of the automated monorail system.

## Directory Structure

```
CAD-Models/
├── README.md                  # This file
├── Monorail_Beam_Assembly/   # Main structural components
├── Sensor_Housings/           # Sensor enclosure designs
├── Control_Units/             # Electronic control units
├── Safety_Systems/            # Emergency and safety components
└── Integration_Models/        # Complete system assemblies
```

## CAD File Types

The following file formats are used in this project:

- **STEP (.step, .stp)**: Standard for the Exchange of Product model data
- **IGES (.igs, .iges)**: Initial Graphics Exchange Specification
- **STL (.stl)**: Stereolithography format for 3D printing
- **DXF (.dxf)**: Drawing Exchange Format for 2D drawings
- **SolidWorks (.sldprt, .sldasm)**: Native SolidWorks files
- **Fusion 360 (.f3d)**: Autodesk Fusion 360 files

## Current CAD Status

The CAD models are currently under development and refinement. Key focus areas include:

1. **Sensor Integration**: Optimizing sensor placement for maximum coverage
2. **Structural Integrity**: Ensuring load-bearing components meet safety standards
3. **Modular Design**: Creating interchangeable components for easier maintenance
4. **Aerodynamic Optimization**: Reducing wind resistance for energy efficiency

## Sensor CAD Refinement Plan

The sensor system CAD models are being refined according to the following priorities:

1. **Primary Sensors**: Distance, speed, and position sensors
2. **Safety Sensors**: Emergency stop and collision avoidance systems
3. **Environmental Sensors**: Temperature, humidity, and atmospheric sensors
4. **Passenger Comfort**: Vibration and noise reduction components

## File Naming Convention

All CAD files should follow this naming convention:

`[SYSTEM]_[COMPONENT]_[VERSION]_[DATE].ext`

Examples:
- `MONORAIL_BEAM_V01_2025-12-23.step`
- `SENSOR_HOUSING_V03_2025-12-23.sldprt`
- `CONTROL_UNIT_V02_2025-12-23.f3d`

## Version Control

Each significant revision should:
1. Increment the version number
2. Update the date stamp
3. Include a changelog entry in the corresponding documentation
4. Maintain backward compatibility where possible

## Validation Process

All CAD models must pass the following validation checks:

1. **Geometry Validation**: No overlapping components, proper clearances
2. **Material Properties**: Correct material assignments and properties
3. **Assembly Constraints**: Proper mating and alignment of components
4. **Manufacturability**: Design for manufacturing (DFM) compliance

## Usage Guidelines

1. **Viewing**: Use appropriate CAD software (SolidWorks, Fusion 360, FreeCAD)
2. **Editing**: Create backup copies before making changes
3. **Sharing**: Export to neutral formats (STEP, IGES) when sharing externally
4. **Documentation**: Update corresponding documentation with any changes

## Contribution

To contribute CAD models:
1. Follow the established naming conventions
2. Include comprehensive documentation
3. Submit models for peer review
4. Update the CAD file summary documentation

## Related Documentation

- [CAD Files Summary](CAD_FILES_SUMMARY.md)
- [Current CAD Status](CURRENT_CAD_STATUS.md)
- [Sensor CAD Refinement Summary](SENSOR_CAD_REFINEMENT_SUMMARY.md)
- [Final CAD Sensor Status](FINAL_CAD_SENSOR_STATUS.md)

## Contact

For CAD-related questions or issues, please contact the engineering team or refer to the main project documentation.
