#!/usr/bin/env python3
"""
WDW Monorail Energy Management System

Monitors and optimizes power consumption across the monorail fleet.
Implements energy-saving strategies and provides power usage analytics.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)sZ %(levelname)s [ENERGY_MANAGEMENT] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("energy_management.log")
    ]
)
logger = logging.getLogger(__name__)


class EnergyConsumptionRecord:
    """Represents energy consumption data for a monorail"""
    
    def __init__(self, monorail_id: str, timestamp: datetime, 
                 power_consumption: float, speed: float, 
                 passengers: int, line: str):
        self.monorail_id = monorail_id
        self.timestamp = timestamp
        self.power_consumption = power_consumption  # in kW
        self.speed = speed  # in mph
        self.passengers = passengers
        self.line = line  # "resort", "express", "epcot_express"
        
    def efficiency_score(self) -> float:
        """Calculate energy efficiency score (passenger-miles per kWh)"""
        if self.power_consumption <= 0:
            return 0.0
        
        # Passenger-miles per hour / kW
        passenger_miles_per_hour = self.passengers * self.speed
        efficiency = passenger_miles_per_hour / self.power_consumption
        
        return round(efficiency, 2)
    
    def to_dict(self) -> Dict:
        return {
            "monorail_id": self.monorail_id,
            "timestamp": self.timestamp.isoformat(),
            "power_consumption": self.power_consumption,
            "speed": self.speed,
            "passengers": self.passengers,
            "line": self.line,
            "efficiency_score": self.efficiency_score()
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            monorail_id=data["monorail_id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            power_consumption=data["power_consumption"],
            speed=data["speed"],
            passengers=data["passengers"],
            line=data["line"]
        )


class EnergyMonitor:
    """Monitors real-time energy consumption for the monorail system"""
    
    def __init__(self):
        self.consumption_records: List[EnergyConsumptionRecord] = []
        self.real_time_data: Dict[str, List[EnergyConsumptionRecord]] = {}
        self.load_data()
        
    def load_data(self):
        """Load energy consumption data from file"""
        try:
            if os.path.exists("energy_data.json"):
                with open("energy_data.json", "r") as f:
                    data = json.load(f)
                    self.consumption_records = [EnergyConsumptionRecord.from_dict(item) for item in data]
                logger.info(f"Loaded {len(self.consumption_records)} energy records")
        except Exception as e:
            logger.error(f"Error loading energy data: {e}")
    
    def save_data(self):
        """Save energy consumption data to file"""
        try:
            with open("energy_data.json", "w") as f:
                json.dump([r.to_dict() for r in self.consumption_records], f, indent=2)
            logger.info(f"Saved {len(self.consumption_records)} energy records")
        except Exception as e:
            logger.error(f"Error saving energy data: {e}")
    
    def add_consumption_record(self, record: EnergyConsumptionRecord):
        """Add a new energy consumption record"""
        self.consumption_records.append(record)
        self.save_data()
    
    def add_real_time_data(self, monorail_id: str, power_consumption: float,
                          speed: float, passengers: int, line: str):
        """Add real-time energy data"""
        record = EnergyConsumptionRecord(
            monorail_id=monorail_id,
            timestamp=datetime.now(),
            power_consumption=power_consumption,
            speed=speed,
            passengers=passengers,
            line=line
        )
        
        self.consumption_records.append(record)
        
        if monorail_id not in self.real_time_data:
            self.real_time_data[monorail_id] = []
        self.real_time_data[monorail_id].append(record)
        
        # Keep only recent data
        if len(self.real_time_data[monorail_id]) > 100:
            self.real_time_data[monorail_id] = self.real_time_data[monorail_id][-100:]
        
        self.save_data()
        return record
    
    def get_recent_consumption(self, monorail_id: str, hours: int = 24) -> List[EnergyConsumptionRecord]:
        """Get recent energy consumption for a monorail"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [r for r in self.consumption_records 
                if r.monorail_id == monorail_id and r.timestamp >= cutoff]
    
    def get_current_power_usage(self) -> Dict[str, float]:
        """Get current power usage for all monorails"""
        current_usage = {}
        
        for monorail_id, records in self.real_time_data.items():
            if records:
                # Get most recent record
                recent = records[-1]
                current_usage[monorail_id] = recent.power_consumption
            else:
                current_usage[monorail_id] = 0.0
        
        return current_usage
    
    def calculate_energy_efficiency(self) -> Dict[str, float]:
        """Calculate energy efficiency for each monorail"""
        efficiency = {}
        
        for monorail_id, records in self.real_time_data.items():
            if records:
                # Calculate average efficiency over recent records
                efficiencies = [r.efficiency_score() for r in records[-10:]]  # Last 10 records
                avg_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0
                efficiency[monorail_id] = round(avg_efficiency, 2)
            else:
                efficiency[monorail_id] = 0.0
        
        return efficiency
    
    def get_energy_savings_opportunities(self) -> List[Dict]:
        """Identify potential energy savings opportunities"""
        opportunities = []
        efficiency = self.calculate_energy_efficiency()
        current_usage = self.get_current_power_usage()
        
        for monorail_id, efficiency_score in efficiency.items():
            current_power = current_usage.get(monorail_id, 0)
            
            if efficiency_score < 5.0:  # Low efficiency threshold
                potential_savings = current_power * 0.15  # Estimate 15% savings
                opportunities.append({
                    "monorail_id": monorail_id,
                    "issue": "Low energy efficiency",
                    "current_efficiency": efficiency_score,
                    "current_power": current_power,
                    "potential_savings_kw": round(potential_savings, 2),
                    "recommendation": "Check motor performance and passenger load"
                })
            
            # Check for high power consumption at low speeds
            recent_records = self.get_recent_consumption(monorail_id, hours=1)
            if recent_records:
                avg_speed = sum(r.speed for r in recent_records) / len(recent_records)
                avg_power = sum(r.power_consumption for r in recent_records) / len(recent_records)
                
                if avg_speed < 10 and avg_power > 80:  # Low speed, high power
                    opportunities.append({
                        "monorail_id": monorail_id,
                        "issue": "High power consumption at low speed",
                        "current_speed": round(avg_speed, 1),
                        "current_power": round(avg_power, 2),
                        "potential_savings_kw": round(avg_power * 0.2, 2),
                        "recommendation": "Investigate motor or braking system"
                    })
        
        return opportunities


class EnergyOptimizer:
    """Optimizes energy consumption across the monorail system"""
    
    def __init__(self, energy_monitor: EnergyMonitor):
        self.monitor = energy_monitor
        self.energy_saving_strategies = {
            "eco_mode": {
                "description": "Reduce max speed by 10%",
                "estimated_savings": 0.12,  # 12% energy savings
                "impact": "Minimal impact on schedule"
            },
            "optimized_acceleration": {
                "description": "Smoother acceleration/deceleration",
                "estimated_savings": 0.08,
                "impact": "Slightly longer travel times"
            },
            "load_balancing": {
                "description": "Distribute passengers evenly",
                "estimated_savings": 0.15,
                "impact": "Better passenger distribution"
            },
            "idle_reduction": {
                "description": "Reduce idle time at stations",
                "estimated_savings": 0.10,
                "impact": "More efficient station operations"
            }
        }
    
    def get_optimization_recommendations(self) -> Dict:
        """Get energy optimization recommendations"""
        opportunities = self.monitor.get_energy_savings_opportunities()
        current_usage = self.monitor.get_current_power_usage()
        total_power = sum(current_usage.values())
        
        recommendations = {
            "current_total_power_kw": round(total_power, 2),
            "average_efficiency": round(np.mean(list(self.monitor.calculate_energy_efficiency().values())), 2),
            "savings_opportunities": opportunities,
            "potential_total_savings_kw": round(sum(op["potential_savings_kw"] for op in opportunities), 2),
            "recommended_strategies": []
        }
        
        # Add recommended strategies based on current conditions
        if opportunities:
            recommendations["recommended_strategies"] = [
                self.energy_saving_strategies["eco_mode"],
                self.energy_saving_strategies["optimized_acceleration"]
            ]
        
        return recommendations
    
    def calculate_optimal_speed(self, current_speed: float, passengers: int) -> float:
        """Calculate optimal speed for energy efficiency"""
        # Base optimal speed curve (passenger-miles per kWh)
        # This is a simplified model - real implementation would use actual data
        
        # For low passenger loads, slower speeds are more efficient
        if passengers < 100:
            return min(current_speed, 25)  # Cap at 25 mph for low loads
        
        # For medium loads, moderate speeds are optimal
        elif passengers < 250:
            optimal = 30  # 30 mph is optimal for medium loads
            return min(current_speed, optimal)
        
        # For high loads, current speed is likely optimal
        else:
            return current_speed
        
        # Note: In a real system, this would use actual energy consumption data
        # and machine learning to determine the true optimal speed
    
    def get_eco_mode_settings(self) -> Dict:
        """Get recommended eco mode settings"""
        return {
            "max_speed_reduction": 0.10,  # 10% reduction
            "acceleration_rate": 0.8,     # 80% of normal
            "deceleration_rate": 0.8,     # 80% of normal
            "idle_timeout": 30,           # 30 seconds before power reduction
            "estimated_savings": 0.12
        }


class EnergyManagementSystem:
    """Main energy management system"""
    
    def __init__(self):
        self.monitor = EnergyMonitor()
        self.optimizer = EnergyOptimizer(self.monitor)
        
    def add_energy_data(self, monorail_id: str, power_consumption: float,
                       speed: float, passengers: int, line: str):
        """Add energy consumption data"""
        return self.monitor.add_real_time_data(
            monorail_id=monorail_id,
            power_consumption=power_consumption,
            speed=speed,
            passengers=passengers,
            line=line
        )
    
    def get_energy_dashboard_data(self) -> Dict:
        """Get data for energy dashboard"""
        return {
            "current_power_usage": self.monitor.get_current_power_usage(),
            "energy_efficiency": self.monitor.calculate_energy_efficiency(),
            "optimization_recommendations": self.optimizer.get_optimization_recommendations(),
            "recent_consumption": {
                monorail_id: [r.to_dict() for r in records[-5:]]  # Last 5 records
                for monorail_id, records in self.monitor.real_time_data.items()
            }
        }
    
    def get_energy_savings_report(self, days: int = 7) -> Dict:
        """Generate an energy savings report"""
        cutoff = datetime.now() - timedelta(days=days)
        recent_records = [r for r in self.monitor.consumption_records if r.timestamp >= cutoff]
        
        if not recent_records:
            return {"error": "No data available for the specified period"}
        
        # Calculate total energy consumption
        total_energy_kwh = sum(r.power_consumption * (1/60) for r in recent_records)  # Convert kW to kWh (assuming 1 minute intervals)
        
        # Calculate average efficiency
        efficiencies = [r.efficiency_score() for r in recent_records]
        avg_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0
        
        # Estimate potential savings
        opportunities = self.monitor.get_energy_savings_opportunities()
        potential_savings_kwh = sum(op["potential_savings_kw"] * 24 * days for op in opportunities)  # Daily savings * days
        
        return {
            "period_days": days,
            "total_energy_consumption_kwh": round(total_energy_kwh, 2),
            "average_efficiency_score": round(avg_efficiency, 2),
            "potential_savings_kwh": round(potential_savings_kwh, 2),
            "potential_savings_percentage": round((potential_savings_kwh / total_energy_kwh) * 100, 1) if total_energy_kwh > 0 else 0,
            "top_opportunities": opportunities[:3],  # Top 3 opportunities
            "energy_consumption_by_line": self._calculate_consumption_by_line(recent_records)
        }
    
    def _calculate_consumption_by_line(self, records: List[EnergyConsumptionRecord]) -> Dict:
        """Calculate energy consumption by line"""
        consumption_by_line = defaultdict(float)
        
        for record in records:
            consumption_by_line[record.line] += record.power_consumption * (1/60)  # kWh
        
        return {line: round(kwh, 2) for line, kwh in consumption_by_line.items()}
    
    async def monitor_energy_consumption(self):
        """Continuously monitor energy consumption"""
        logger.info("Starting energy consumption monitoring...")
        
        while True:
            try:
                # Get current energy status
                dashboard_data = self.get_energy_dashboard_data()
                
                # Check for critical energy issues
                opportunities = dashboard_data["optimization_recommendations"]["savings_opportunities"]
                
                if opportunities:
                    for op in opportunities:
                        if op["potential_savings_kw"] > 50:  # Significant savings
                            logger.warning(f"ENERGY ALERT: {op['monorail_id']} - {op['issue']} (Potential savings: {op['potential_savings_kw']} kW)")
                
                # Log current energy status
                total_power = sum(dashboard_data["current_power_usage"].values())
                avg_efficiency = np.mean(list(dashboard_data["energy_efficiency"].values()))
                
                logger.info(f"Current energy status - Total: {total_power:.1f} kW, Avg Efficiency: {avg_efficiency:.1f}")
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in energy monitoring: {e}")
                await asyncio.sleep(60)


async def main():
    """Main entry point for testing"""
    # Initialize system
    ems = EnergyManagementSystem()
    
    # Add some sample data if none exists
    if not ems.monitor.consumption_records:
        logger.info("Adding sample energy data...")
        
        now = datetime.now()
        sample_data = []
        
        # Sample data for different monorails and conditions
        for hour in range(24):
            timestamp = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Peak hours (8-10 AM, 4-6 PM) - higher power consumption
            if 8 <= hour <= 10 or 16 <= hour <= 18:
                sample_data.extend([
                    EnergyConsumptionRecord("monorail_red", timestamp, 120.0, 32.0, 280, "express"),
                    EnergyConsumptionRecord("monorail_blue", timestamp, 110.0, 30.0, 260, "resort"),
                    EnergyConsumptionRecord("monorail_green", timestamp, 115.0, 31.0, 270, "express"),
                ])
            
            # Off-peak hours - lower power consumption
            else:
                sample_data.extend([
                    EnergyConsumptionRecord("monorail_red", timestamp, 80.0, 25.0, 150, "express"),
                    EnergyConsumptionRecord("monorail_blue", timestamp, 75.0, 22.0, 120, "resort"),
                    EnergyConsumptionRecord("monorail_green", timestamp, 78.0, 23.0, 130, "epcot_express"),
                ])
        
        for record in sample_data:
            ems.monitor.add_consumption_record(record)
    
    # Test energy monitoring
    logger.info("Energy Monitoring Analysis:")
    logger.info(f"Current power usage: {ems.monitor.get_current_power_usage()}")
    logger.info(f"Energy efficiency: {ems.monitor.calculate_energy_efficiency()}")
    
    # Test optimization
    logger.info("\nEnergy Optimization Recommendations:")
    recommendations = ems.optimizer.get_optimization_recommendations()
    for key, value in recommendations.items():
        if key != "savings_opportunities":
            logger.info(f"{key}: {value}")
        else:
            logger.info(f"{key}: {len(value)} opportunities found")
    
    # Test dashboard data
    logger.info("\nEnergy Dashboard Data:")
    dashboard_data = ems.get_energy_dashboard_data()
    logger.info(f"Current power usage: {dashboard_data['current_power_usage']}")
    logger.info(f"Energy efficiency: {dashboard_data['energy_efficiency']}")
    
    # Test energy savings report
    logger.info("\nEnergy Savings Report (7 days):")
    report = ems.get_energy_savings_report(days=7)
    for key, value in report.items():
        if key != "top_opportunities":
            logger.info(f"{key}: {value}")
        else:
            logger.info(f"{key}: {len(value)} top opportunities")
    
    # Start monitoring (in a real system, this would run continuously)
    # await ems.monitor_energy_consumption()


if __name__ == "__main__":
    asyncio.run(main())
