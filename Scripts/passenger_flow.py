#!/usr/bin/env python3
"""
WDW Monorail Passenger Flow Optimization System

Analyzes passenger data and optimizes monorail scheduling and routing
for better crowd management and passenger experience.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)sZ %(levelname)s [PASSENGER_FLOW] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("passenger_flow.log")
    ]
)
logger = logging.getLogger(__name__)


class PassengerData:
    """Represents passenger count data for a specific location and time"""
    
    def __init__(self, station: str, timestamp: datetime, 
                 passengers_in: int, passengers_out: int):
        self.station = station
        self.timestamp = timestamp
        self.passengers_in = passengers_in
        self.passengers_out = passengers_out
        
    @property
    def net_passengers(self) -> int:
        return self.passengers_in - self.passengers_out
    
    @property
    def total_passengers(self) -> int:
        return self.passengers_in + self.passengers_out
    
    def to_dict(self) -> Dict:
        return {
            "station": self.station,
            "timestamp": self.timestamp.isoformat(),
            "passengers_in": self.passengers_in,
            "passengers_out": self.passengers_out
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            station=data["station"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            passengers_in=data["passengers_in"],
            passengers_out=data["passengers_out"]
        )


class PassengerFlowAnalyzer:
    """Analyzes passenger flow patterns and provides insights"""
    
    def __init__(self):
        self.passenger_data: List[PassengerData] = []
        self.stations = ["TTC", "Poly", "GF", "MK", "Epcot", "HS"]
        self.load_data()
        
    def load_data(self):
        """Load passenger data from file"""
        try:
            if os.path.exists("passenger_data.json"):
                with open("passenger_data.json", "r") as f:
                    data = json.load(f)
                    self.passenger_data = [PassengerData.from_dict(item) for item in data]
                logger.info(f"Loaded {len(self.passenger_data)} passenger records")
        except Exception as e:
            logger.error(f"Error loading passenger data: {e}")
    
    def save_data(self):
        """Save passenger data to file"""
        try:
            with open("passenger_data.json", "w") as f:
                json.dump([p.to_dict() for p in self.passenger_data], f, indent=2)
            logger.info(f"Saved {len(self.passenger_data)} passenger records")
        except Exception as e:
            logger.error(f"Error saving passenger data: {e}")
    
    def add_passenger_data(self, data: PassengerData):
        """Add new passenger data"""
        self.passenger_data.append(data)
        self.save_data()
    
    def get_passenger_counts_by_station(self, station: str, 
                                       hours: int = 24) -> List[PassengerData]:
        """Get passenger data for a specific station"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [d for d in self.passenger_data 
                if d.station == station and d.timestamp >= cutoff]
    
    def get_hourly_averages(self) -> Dict[str, Dict[int, float]]:
        """Calculate average passenger counts by hour for each station"""
        hourly_averages = defaultdict(lambda: defaultdict(list))
        
        for data in self.passenger_data:
            hour = data.timestamp.hour
            hourly_averages[data.station][hour].append(data.total_passengers)
        
        result = {}
        for station, hours in hourly_averages.items():
            result[station] = {}
            for hour, counts in hours.items():
                result[station][hour] = sum(counts) / len(counts)
        
        return result
    
    def identify_peak_hours(self) -> Dict[str, List[int]]:
        """Identify peak hours for each station"""
        hourly_avgs = self.get_hourly_averages()
        peak_hours = {}
        
        for station, hours in hourly_avgs.items():
            if not hours:
                continue
            
            avg_count = sum(hours.values()) / len(hours)
            peak_hours[station] = [
                hour for hour, count in hours.items()
                if count > avg_count * 1.5  # 50% above average
            ]
        
        return peak_hours
    
    def calculate_crowding_index(self) -> Dict[str, float]:
        """Calculate a crowing index for each station (0-1 scale)"""
        hourly_avgs = self.get_hourly_averages()
        crowing_index = {}
        
        for station, hours in hourly_avgs.items():
            if not hours:
                crowing_index[station] = 0.0
                continue
            
            max_hour = max(hours.values())
            avg_hour = sum(hours.values()) / len(hours)
            
            # Crowding index: ratio of peak to average, normalized to 0-1
            if avg_hour > 0:
                index = min(1.0, (max_hour - avg_hour) / (avg_hour * 2))
                crowing_index[station] = round(index, 3)
            else:
                crowing_index[station] = 0.0
        
        return crowing_index
    
    def predict_future_flow(self, station: str, hours_ahead: int = 2) -> float:
        """Predict passenger flow for a station in the near future"""
        # Simple prediction based on historical patterns
        now = datetime.now()
        current_hour = now.hour
        future_hour = (current_hour + hours_ahead) % 24
        
        hourly_avgs = self.get_hourly_averages()
        station_data = hourly_avgs.get(station, {})
        
        if future_hour in station_data:
            return station_data[future_hour]
        
        # Fallback: use average of nearby hours
        nearby_hours = [h for h in range(future_hour-1, future_hour+2) if h in station_data]
        if nearby_hours:
            return sum(station_data[h] for h in nearby_hours) / len(nearby_hours)
        
        return 0.0


class RouteOptimizer:
    """Optimizes monorail routes based on passenger demand"""
    
    def __init__(self, passenger_analyzer: PassengerFlowAnalyzer):
        self.analyzer = passenger_analyzer
        self.current_routes = {
            "resort": ["TTC", "Poly", "GF", "MK"],
            "express": ["TTC", "MK", "Epcot", "HS"],
            "epcot_express": ["TTC", "Epcot"]
        }
        self.train_capacity = 300  # passengers per train
        
    def optimize_routes(self) -> Dict[str, List[str]]:
        """Optimize routes based on current passenger demand"""
        # Get current passenger demand
        crowing_index = self.analyzer.calculate_crowding_index()
        peak_hours = self.analyzer.identify_peak_hours()
        
        # Simple optimization: add more trains to crowded routes
        optimized_routes = {}
        
        for route_name, stations in self.current_routes.items():
            # Calculate route demand based on station crowing
            route_demand = sum(crowing_index.get(station, 0) for station in stations)
            
            # If high demand, consider adding express routes or more frequent service
            if route_demand > 1.5:  # High demand threshold
                # Add express service for busy stations
                if route_name == "resort":
                    # Add direct TTC->MK service during peak hours
                    if "MK" in peak_hours and len(peak_hours["MK"]) > 0:
                        optimized_routes["resort_express"] = ["TTC", "MK"]
                
                elif route_name == "express":
                    # Add more frequent service
                    optimized_routes["express_frequent"] = stations
            
            optimized_routes[route_name] = stations
        
        return optimized_routes
    
    def calculate_train_allocation(self) -> Dict[str, int]:
        """Calculate optimal train allocation per route"""
        crowing_index = self.analyzer.calculate_crowding_index()
        
        # Base allocation
        allocation = {
            "resort": 4,
            "express": 4,
            "epcot_express": 2
        }
        
        # Adjust based on demand
        resort_demand = sum(crowing_index.get(s, 0) for s in ["TTC", "Poly", "GF", "MK"])
        express_demand = sum(crowing_index.get(s, 0) for s in ["TTC", "MK", "Epcot", "HS"])
        
        # Total trains available: 12
        total_trains = 12
        
        # Adjust allocation based on relative demand
        if resort_demand > express_demand * 1.2:
            allocation["resort"] = min(6, allocation["resort"] + 1)
            allocation["express"] = max(2, allocation["express"] - 1)
        elif express_demand > resort_demand * 1.2:
            allocation["express"] = min(6, allocation["express"] + 1)
            allocation["resort"] = max(2, allocation["resort"] - 1)
        
        # Ensure we don't exceed total trains
        current_total = sum(allocation.values())
        if current_total > total_trains:
            # Reduce from routes with lower demand
            if resort_demand < express_demand:
                allocation["resort"] = max(2, allocation["resort"] - (current_total - total_trains))
            else:
                allocation["express"] = max(2, allocation["express"] - (current_total - total_trains))
        
        return allocation
    
    def get_recommended_headway(self, route_name: str) -> int:
        """Get recommended time between trains (in minutes)"""
        # Base headway
        base_headways = {
            "resort": 10,
            "express": 8,
            "epcot_express": 15
        }
        
        # Get current demand
        stations = self.current_routes.get(route_name, [])
        crowing_index = self.analyzer.calculate_crowding_index()
        route_demand = sum(crowing_index.get(s, 0) for s in stations)
        
        # Adjust headway based on demand
        if route_demand > 1.8:
            # Very high demand - reduce headway
            return max(5, base_headways[route_name] - 3)
        elif route_demand > 1.2:
            # High demand - reduce headway slightly
            return max(7, base_headways[route_name] - 2)
        elif route_demand < 0.5:
            # Low demand - increase headway
            return min(20, base_headways[route_name] + 5)
        else:
            # Normal demand
            return base_headways[route_name]


class PassengerFlowOptimizationSystem:
    """Main passenger flow optimization system"""
    
    def __init__(self):
        self.analyzer = PassengerFlowAnalyzer()
        self.optimizer = RouteOptimizer(self.analyzer)
        self.real_time_data = defaultdict(list)
        
    def add_real_time_data(self, station: str, passengers_in: int, passengers_out: int):
        """Add real-time passenger data"""
        data = PassengerData(
            station=station,
            timestamp=datetime.now(),
            passengers_in=passengers_in,
            passengers_out=passengers_out
        )
        self.analyzer.add_passenger_data(data)
        self.real_time_data[station].append(data)
        
        # Keep only recent data
        if len(self.real_time_data[station]) > 100:
            self.real_time_data[station] = self.real_time_data[station][-100:]
    
    def get_current_crowding(self) -> Dict[str, Dict]:
        """Get current crowing status for all stations"""
        crowing_status = {}
        
        for station in self.analyzer.stations:
            recent_data = [d for d in self.real_time_data.get(station, [])
                          if d.timestamp >= datetime.now() - timedelta(hours=1)]
            
            if recent_data:
                total_in = sum(d.passengers_in for d in recent_data)
                total_out = sum(d.passengers_out for d in recent_data)
                net = total_in - total_out
                
                # Estimate current passengers at station
                current_passengers = max(0, net)
                
                # Crowding level
                if current_passengers > 500:
                    level = "high"
                elif current_passengers > 200:
                    level = "medium"
                else:
                    level = "low"
                
                crowing_status[station] = {
                    "current_passengers": current_passengers,
                    "level": level,
                    "last_updated": recent_data[-1].timestamp.isoformat()
                }
            else:
                crowing_status[station] = {
                    "current_passengers": 0,
                    "level": "unknown",
                    "last_updated": None
                }
        
        return crowing_status
    
    def get_optimization_recommendations(self) -> Dict:
        """Get current optimization recommendations"""
        return {
            "route_optimization": self.optimizer.optimize_routes(),
            "train_allocation": self.optimizer.calculate_train_allocation(),
            "recommended_headways": {
                route: self.optimizer.get_recommended_headway(route)
                for route in ["resort", "express", "epcot_express"]
            },
            "peak_hours": self.analyzer.identify_peak_hours(),
            "crowding_index": self.analyzer.calculate_crowding_index()
        }
    
    async def monitor_passenger_flow(self):
        """Continuously monitor passenger flow"""
        logger.info("Starting passenger flow monitoring...")
        
        while True:
            try:
                # Get current status
                crowing = self.get_current_crowding()
                recommendations = self.get_optimization_recommendations()
                
                # Log any critical situations
                for station, status in crowing.items():
                    if status["level"] == "high":
                        logger.warning(f"HIGH CROWING at {station}: {status['current_passengers']} passengers")
                
                # Log optimization recommendations
                logger.info(f"Current recommendations: {recommendations}")
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Error in passenger flow monitoring: {e}")
                await asyncio.sleep(60)


async def main():
    """Main entry point for testing"""
    # Initialize system
    pfo = PassengerFlowOptimizationSystem()
    
    # Add some sample data if none exists
    if not pfo.analyzer.passenger_data:
        logger.info("Adding sample passenger data...")
        
        now = datetime.now()
        sample_data = []
        
        # Sample data for different times of day
        for hour in range(24):
            timestamp = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            
            # Morning rush (8-10 AM)
            if 8 <= hour <= 10:
                sample_data.extend([
                    PassengerData("TTC", timestamp, 150, 80),
                    PassengerData("MK", timestamp, 200, 120),
                    PassengerData("Epcot", timestamp, 120, 90),
                ])
            
            # Midday (11 AM - 3 PM)
            elif 11 <= hour <= 15:
                sample_data.extend([
                    PassengerData("TTC", timestamp, 80, 60),
                    PassengerData("MK", timestamp, 150, 100),
                    PassengerData("Epcot", timestamp, 90, 70),
                    PassengerData("HS", timestamp, 60, 40),
                ])
            
            # Evening rush (4-6 PM)
            elif 16 <= hour <= 18:
                sample_data.extend([
                    PassengerData("MK", timestamp, 180, 150),
                    PassengerData("Epcot", timestamp, 140, 110),
                    PassengerData("TTC", timestamp, 120, 90),
                ])
            
            # Night (7 PM - 7 AM)
            else:
                sample_data.extend([
                    PassengerData("TTC", timestamp, 20, 30),
                    PassengerData("MK", timestamp, 30, 40),
                ])
        
        for data in sample_data:
            pfo.analyzer.add_passenger_data(data)
    
    # Test analysis
    logger.info("Passenger Flow Analysis:")
    logger.info(f"Hourly averages: {pfo.analyzer.get_hourly_averages()}")
    logger.info(f"Peak hours: {pfo.analyzer.identify_peak_hours()}")
    logger.info(f"Crowing index: {pfo.analyzer.calculate_crowding_index()}")
    
    # Test optimization
    logger.info("\nOptimization Recommendations:")
    recommendations = pfo.get_optimization_recommendations()
    for section, data in recommendations.items():
        logger.info(f"{section}: {data}")
    
    # Test real-time monitoring
    logger.info("\nTesting real-time monitoring...")
    
    # Simulate some real-time data
    pfo.add_real_time_data("MK", 85, 60)
    pfo.add_real_time_data("Epcot", 70, 45)
    pfo.add_real_time_data("TTC", 60, 30)
    
    logger.info(f"Current crowing: {pfo.get_current_crowding()}")
    
    # Start monitoring (in a real system, this would run continuously)
    # await pfo.monitor_passenger_flow()


if __name__ == "__main__":
    asyncio.run(main())
