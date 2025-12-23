#!/usr/bin/env python3
"""
WDW Monorail System - Sensor Coverage Validator

This script validates that the sensor coverage meets all minimum requirements
before the system can be finalized for version control.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List

class SensorCoverageValidator:
    def __init__(self):
        self.min_requirements = {
            "monorails": {
                "min_count": 9,
                "min_sensors_per_monorail": 2,
                "total_min_sensors": 18
            },
            "stations": {
                "resort_hotels": {"min_count": 3, "min_sensors": 6},
                "epcot": {"min_count": 1, "min_sensors": 3},
                "ttc": {"min_count": 1, "min_sensors": 6}
            },
            "maintenance": {
                "min_sensors": 2
            },
            "barn": {
                "min_sensors": 4
            },
            "total": {
                "min_sensors": 36,
                "max_sensors": 50
            }
        }
        
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }
    
    def load_sensor_data(self, file_path: str) -> Dict[str, Any]:
        """Load sensor data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.results["failed"].append(f"Failed to load sensor data: {e}")
            return {}
    
    def validate_monorail_coverage(self, sensor_data: Dict[str, Any]) -> bool:
        """Validate monorail sensor coverage"""
        monorails = sensor_data.get("monorails", {})
        
        # Check minimum monorail count
        if len(monorails) < self.min_requirements["monorails"]["min_count"]:
            self.results["failed"].append(
                f"Insufficient monorails: {len(monorails)} (min {self.min_requirements['monorails']['min_count']})"
            )
            return False
        
        # Check sensors per monorail
        total_monorail_sensors = 0
        for monorail_id, monorail_data in monorails.items():
            sensors = monorail_data.get("onboard_sensors", {})
            sensor_count = len(sensors)
            total_monorail_sensors += sensor_count
            
            if sensor_count < self.min_requirements["monorails"]["min_sensors_per_monorail"]:
                self.results["failed"].append(
                    f"Monorail {monorail_id} has only {sensor_count} sensors "
                    f"(min {self.min_requirements['monorails']['min_sensors_per_monorail']})"
                )
        
        # Check total monorail sensors
        if total_monorail_sensors < self.min_requirements["monorails"]["total_min_sensors"]:
            self.results["failed"].append(
                f"Total monorail sensors: {total_monorail_sensors} "
                f"(min {self.min_requirements['monorails']['total_min_sensors']})"
            )
        else:
            self.results["passed"].append(
                f"Monorail coverage: {total_monorail_sensors} sensors "
                f"({len(monorails)} monorails, avg {total_monorail_sensors/len(monorails):.1f} per monorail)"
            )
        
        return len(self.results["failed"]) == 0
    
    def validate_station_coverage(self, sensor_data: Dict[str, Any]) -> bool:
        """Validate station sensor coverage"""
        stations = sensor_data.get("stations", {})
        
        # Check resort hotels
        resort_stations = [s for s in stations.values() if s.get("type") == "Resort"]
        if len(resort_stations) < self.min_requirements["stations"]["resort_hotels"]["min_count"]:
            self.results["failed"].append(
                f"Insufficient resort stations: {len(resort_stations)} "
                f"(min {self.min_requirements['stations']['resort_hotels']['min_count']})"
            )
        
        # Check Epcot station
        epcot_stations = [s for s in stations.values() if s.get("type", "").lower() in ["epcot", "major"]]
        if len(epcot_stations) < self.min_requirements["stations"]["epcot"]["min_count"]:
            self.results["failed"].append(
                f"Insufficient Epcot stations: {len(epcot_stations)} "
                f"(min {self.min_requirements['stations']['epcot']['min_count']})"
            )
        
        # Check TTC - it might be in the stations dict or as a separate top-level key
        ttc_stations = [s for s in stations.values() if s.get("type", "").lower() in ["ttc", "central", "hub"]]
        if len(ttc_stations) < self.min_requirements["stations"]["ttc"]["min_count"]:
            # Also check if TTC exists as a top-level key
            if "ttc" in sensor_data and len(sensor_data["ttc"].get("sensors", {})) >= 6:
                # TTC exists at top level with sufficient sensors
                ttc_stations = [{"id": "TTC", "type": "TTC"}]
            else:
                self.results["failed"].append(
                    f"Insufficient TTC stations: {len(ttc_stations)} "
                    f"(min {self.min_requirements['stations']['ttc']['min_count']})"
                )
        
        # Check sensor counts
        total_station_sensors = 0
        for station_id, station_data in stations.items():
            sensors = station_data.get("sensors", {})
            sensor_count = len(sensors)
            total_station_sensors += sensor_count
            
            station_type = station_data.get("type", "Unknown").lower()
            if station_type in ["resort", "hotel"] and sensor_count < 2:
                self.results["failed"].append(
                    f"Resort station {station_id} has only {sensor_count} sensors (min 2)"
                )
            elif station_type in ["epcot", "major"] and sensor_count < 3:
                self.results["failed"].append(
                    f"Epcot station {station_id} has only {sensor_count} sensors (min 3)"
                )
            elif station_type in ["ttc", "central", "hub"] and sensor_count < 6:
                self.results["failed"].append(
                    f"TTC station {station_id} has only {sensor_count} sensors (min 6)"
                )
        
        # Add TTC sensors from top-level if present
        if "ttc" in sensor_data and "sensors" in sensor_data["ttc"]:
            total_station_sensors += len(sensor_data["ttc"]["sensors"])
        
        if len(self.results["failed"]) == 0:
            self.results["passed"].append(
                f"Station coverage: {total_station_sensors} sensors "
                f"({len(stations)} stations + {'TTC' if 'ttc' in sensor_data else ''})"
            )
        
        return len(self.results["failed"]) == 0
    
    def validate_maintenance_coverage(self, sensor_data: Dict[str, Any]) -> bool:
        """Validate maintenance sensor coverage"""
        maintenance = sensor_data.get("maintenance", {})
        sensors = maintenance.get("sensors", {})
        
        if len(sensors) < self.min_requirements["maintenance"]["min_sensors"]:
            self.results["failed"].append(
                f"Insufficient maintenance sensors: {len(sensors)} "
                f"(min {self.min_requirements['maintenance']['min_sensors']})"
            )
            return False
        
        self.results["passed"].append(
            f"Maintenance coverage: {len(sensors)} sensors"
        )
        return True
    
    def validate_barn_coverage(self, sensor_data: Dict[str, Any]) -> bool:
        """Validate barn sensor coverage"""
        barn = sensor_data.get("barn", {})
        sensors = barn.get("sensors", {})
        
        if len(sensors) < self.min_requirements["barn"]["min_sensors"]:
            self.results["failed"].append(
                f"Insufficient barn sensors: {len(sensors)} "
                f"(min {self.min_requirements['barn']['min_sensors']})"
            )
            return False
        
        self.results["passed"].append(
            f"Barn coverage: {len(sensors)} sensors"
        )
        return True
    
    def validate_total_coverage(self, sensor_data: Dict[str, Any]) -> bool:
        """Validate total sensor coverage"""
        # Count all sensors
        total_sensors = 0
        
        # Monorail sensors
        for monorail_data in sensor_data.get("monorails", {}).values():
            total_sensors += len(monorail_data.get("onboard_sensors", {}))
        
        # Station sensors
        for station_data in sensor_data.get("stations", {}).values():
            total_sensors += len(station_data.get("sensors", {}))
        
        # TTC sensors (top-level)
        total_sensors += len(sensor_data.get("ttc", {}).get("sensors", {}))
        
        # Maintenance sensors
        total_sensors += len(sensor_data.get("maintenance", {}).get("sensors", {}))
        
        # Barn sensors
        total_sensors += len(sensor_data.get("barn", {}).get("sensors", {}))
        
        print(f"DEBUG: Total sensors counted: {total_sensors}")  # Debug line
        
        # Check minimum
        if total_sensors < self.min_requirements["total"]["min_sensors"]:
            self.results["failed"].append(
                f"Insufficient total sensors: {total_sensors} "
                f"(min {self.min_requirements['total']['min_sensors']})"
            )
            return False
        
        # Check maximum (warning only)
        if total_sensors > self.min_requirements["total"]["max_sensors"]:
            self.results["warnings"].append(
                f"High sensor count: {total_sensors} "
                f"(max recommended {self.min_requirements['total']['max_sensors']})"
            )
        
        self.results["passed"].append(
            f"Total coverage: {total_sensors} sensors "
            f"(within {self.min_requirements['total']['min_sensors']}-{self.min_requirements['total']['max_sensors']} range)"
        )
        
        return True
    
    def run_validation(self, sensor_data_file: str) -> bool:
        """Run complete validation"""
        print("🔍 WDW Monorail Sensor Coverage Validator")
        print("=" * 50)
        
        # Load data
        sensor_data = self.load_sensor_data(sensor_data_file)
        if not sensor_data:
            return False
        
        # Run validations
        print("\n📊 Running validation checks...")
        
        self.validate_monorail_coverage(sensor_data)
        self.validate_station_coverage(sensor_data)
        self.validate_maintenance_coverage(sensor_data)
        self.validate_barn_coverage(sensor_data)
        self.validate_total_coverage(sensor_data)
        
        # Print results
        print("\n✅ Passed Checks:")
        for check in self.results["passed"]:
            print(f"  ✓ {check}")
        
        if self.results["warnings"]:
            print("\n⚠️  Warnings:")
            for warning in self.results["warnings"]:
                print(f"  ⚠ {warning}")
        
        if self.results["failed"]:
            print("\n❌ Failed Checks:")
            for failure in self.results["failed"]:
                print(f"  ✗ {failure}")
        
        # Summary
        total_checks = len(self.results["passed"]) + len(self.results["failed"])
        passed_checks = len(self.results["passed"])
        
        print("\n" + "=" * 50)
        print(f"📈 Validation Summary: {passed_checks}/{total_checks} checks passed")
        
        if len(self.results["failed"]) > 0:
            print("❌ Sensor coverage does NOT meet requirements!")
            return False
        else:
            print("✅ Sensor coverage meets all requirements!")
            if self.results["warnings"]:
                print("⚠️  Some warnings detected (see above)")
            return True
    
    def generate_report(self, output_file: str):
        """Generate validation report"""
        report = {
            "validation_results": self.results,
            "requirements": self.min_requirements,
            "timestamp": str(Path(output_file).stat().st_mtime) if Path(output_file).exists() else "N/A"
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Validation report saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sensor_coverage_validator.py <sensor_data_file.json>")
        sys.exit(1)
    
    validator = SensorCoverageValidator()
    success = validator.run_validation(sys.argv[1])
    
    # Generate report
    report_file = sys.argv[1].replace(".json", "_validation_report.json")
    validator.generate_report(report_file)
    
    sys.exit(0 if success else 1)



