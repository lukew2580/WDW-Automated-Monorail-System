#!/usr/bin/env python3
"""
WDW Monorail System - CAD File Validator

This script validates that CAD files exist and meet basic requirements
for the monorail system development.
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class CADFileValidator:
    def __init__(self):
        self.required_files = {
            "barn": {
                "path": "Monorail-Barn/barn_3d_model.blend",
                "size_min": 1024,  # 1KB minimum
                "required": True,
                "description": "Main barn structure with 6 beams and 12 parking slots"
            },
            "barn_render": {
                "path": "Monorail-Barn/barn_3d_model.png",
                "size_min": 10240,  # 10KB minimum
                "required": True,
                "description": "Rendered image of barn model"
            },
            "monorail_vehicles": {
                "path": "Monorail-Vehicles/*.blend",
                "count": 12,
                "size_min": 51200,  # 50KB minimum per vehicle
                "required": False,  # Not yet created
                "description": "12 monorail vehicle models (M1-M12)"
            },
            "stations": {
                "path": "Stations/*.blend",
                "count": 4,
                "size_min": 102400,  # 100KB minimum per station
                "required": False,  # Not yet created
                "description": "4 station models (Polynesian, Grand Floridian, Contemporary, Epcot)"
            },
            "track_system": {
                "path": "Track/*.blend",
                "count": 1,
                "size_min": 51200,  # 50KB minimum
                "required": False,  # Not yet created
                "description": "Complete track system model"
            },
            "ttc": {
                "path": "TTC/ttc_model.blend",
                "size_min": 102400,  # 100KB minimum
                "required": False,  # Not yet created
                "description": "Ticket & Transportation Center model"
            },
            "maintenance": {
                "path": "Maintenance/maintenance_facility.blend",
                "size_min": 51200,  # 50KB minimum
                "required": False,  # Not yet created
                "description": "Maintenance facility model"
            }
        }
        
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": [],
            "info": []
        }
        
        self.stats = {
            "total_files": 0,
            "existing_files": 0,
            "missing_files": 0,
            "total_size": 0
        }
    
    def check_file_exists(self, file_path):
        """Check if file exists and get its size"""
        full_path = os.path.join("/home/workspace/WDW-Monorail-System", file_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            return True, size
        return False, 0
    
    def validate_blender_file(self, file_path):
        """Validate Blender file structure using Blender CLI"""
        try:
            full_path = os.path.join("/home/workspace/WDW-Monorail-System", file_path)
            cmd = [
                "blender", "--background", full_path, "--python-expr",
                "import bpy; print('VALID:' + str(len(bpy.data.objects)) + ':' + str(len(bpy.data.meshes)))"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "VALID:" in result.stdout:
                parts = result.stdout.strip().split(":")
                if len(parts) >= 3:
                    return True, int(parts[1]), int(parts[2])
            
            return False, 0, 0
            
        except Exception as e:
            return False, 0, 0
    
    def run_validation(self):
        """Run comprehensive CAD file validation"""
        print("🔍 WDW Monorail CAD File Validator")
        print("=" * 50)
        
        for file_key, file_info in self.required_files.items():
            exists, size = self.check_file_exists(file_info["path"])
            self.stats["total_files"] += 1
            
            if exists:
                self.stats["existing_files"] += 1
                self.stats["total_size"] += size
                
                # Check size requirements
                if size >= file_info.get("size_min", 0):
                    self.results["passed"].append(f"✅ {file_key}: {file_info['description']} ({size/1024:.1f} KB)")
                    
                    # Validate Blender files
                    if file_key.startswith("barn") and file_info["path"].endswith(".blend"):
                        valid, obj_count, mesh_count = self.validate_blender_file(file_info["path"])
                        if valid:
                            self.results["passed"].append(f"✅ {file_key} structure: {obj_count} objects, {mesh_count} meshes")
                        else:
                            self.results["warnings"].append(f"⚠️  {file_key} structure validation failed")
                else:
                    self.results["failed"].append(f"❌ {file_key}: Too small ({size/1024:.1f} KB < {file_info.get('size_min',0)/1024:.1f} KB)")
            else:
                self.stats["missing_files"] += 1
                if file_info["required"]:
                    self.results["failed"].append(f"❌ {file_key}: MISSING - {file_info['description']}")
                else:
                    self.results["warnings"].append(f"⚠️  {file_key}: Not yet created - {file_info['description']}")
        
        # Calculate completion percentage
        completion = (self.stats["existing_files"] / self.stats["total_files"]) * 100 if self.stats["total_files"] > 0 else 0
        
        return completion >= 100  # Only pass if all required files exist
    
    def print_results(self):
        """Print validation results"""
        print("\n📊 Validation Results:")
        print("-" * 40)
        
        for result in self.results["passed"]:
            print(result)
        
        for result in self.results["failed"]:
            print(result)
        
        for result in self.results["warnings"]:
            print(result)
        
        print("\n📈 Statistics:")
        print(f"  Total files checked: {self.stats['total_files']}")
        print(f"  Existing files: {self.stats['existing_files']}")
        print(f"  Missing files: {self.stats['missing_files']}")
        print(f"  Total size: {self.stats['total_size']/1024:.1f} KB ({self.stats['total_size']/1024/1024:.2f} MB)")
        
        completion = (self.stats["existing_files"] / self.stats["total_files"]) * 100 if self.stats["total_files"] > 0 else 0
        print(f"  Completion: {completion:.1f}%")
        
        # Print summary
        if len(self.results["failed"]) == 0 and len(self.results["warnings"]) == 0:
            print(f"\n✅ All CAD files validated successfully!")
        elif len(self.results["failed"]) > 0:
            print(f"\n❌ CAD validation failed - {len(self.results['failed'])} critical issues")
        else:
            print(f"\n⚠️  CAD validation partial - {len(self.results['warnings'])} warnings")
    
    def generate_report(self, output_file):
        """Generate validation report"""
        report = {
            "validation_results": self.results,
            "statistics": self.stats,
            "completion_percentage": (self.stats["existing_files"] / self.stats["total_files"]) * 100 if self.stats["total_files"] > 0 else 0,
            "timestamp": "2025-12-22"
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Validation report saved to: {output_file}")

if __name__ == "__main__":
    validator = CADFileValidator()
    success = validator.run_validation()
    validator.print_results()
    validator.generate_report("/home/workspace/WDW-Automated-Monorail-System/cad_validation_report.json")
    
    sys.exit(0 if success else 1)








