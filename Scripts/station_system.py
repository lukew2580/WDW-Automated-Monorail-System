#!/usr/bin/env python3
"""
Monorail Station System
Manages stops, boarding, and station-to-station automation
"""

import json
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import asyncio

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

class StationStatus(Enum):
    IDLE = "idle"
    BOARDING = "boarding"
    DOORS_CLOSING = "doors_closing"
    DEPARTING = "departing"
    IN_TRANSIT = "in_transit"
    ARRIVING = "arriving"

@dataclass
class Station:
    name: str
    position: float  # Distance from start (meters)
    stop_duration: int  # Seconds to stay
    passengers_waiting: int = 0
    status: StationStatus = StationStatus.IDLE

class StationSystem:
    def __init__(self):
        self.stations = {
            "magic_kingdom": Station("Magic Kingdom", 0, 20),
            "epcot": Station("Epcot", 2500, 20),
            "hollywood_studios": Station("Hollywood Studios", 5000, 20),
            "animal_kingdom": Station("Animal Kingdom", 7500, 20),
            "ttr": Station("Transportation & Ticket Center", 10000, 30),
        }
        self.current_station = None
        self.next_station = None
        self.monorail_position = 0
        self.total_distance = 10000
        self.is_running = False
        
        logging.info("Station System initialized")
        
    async def board_passengers(self, station_name: str, count: int):
        """Simulate passenger boarding"""
        if station_name in self.stations:
            station = self.stations[station_name]
            station.passengers_waiting = count
            station.status = StationStatus.BOARDING
            logging.info(f"[{station_name}] Boarding {count} passengers")
            await asyncio.sleep(5)  # Simulate boarding time
            station.status = StationStatus.DOORS_CLOSING
            logging.info(f"[{station_name}] Doors closing")
            await asyncio.sleep(2)
            station.status = StationStatus.DEPARTING
            return True
        return False
    
    async def arrive_at_station(self, station_name: str):
        """Monorail arrives at a station"""
        if station_name in self.stations:
            station = self.stations[station_name]
            self.current_station = station_name
            station.status = StationStatus.ARRIVING
            logging.info(f"ARRIVING at {station.name}")
            await asyncio.sleep(3)
            station.status = StationStatus.BOARDING
            return station
        return None
    
    async def depart_from_station(self, station_name: str, next_station: str):
        """Depart from current station to next"""
        if station_name in self.stations and next_station in self.stations:
            current = self.stations[station_name]
            nxt = self.stations[next_station]
            current.status = StationStatus.DEPARTING
            self.next_station = next_station
            
            distance = abs(nxt.position - current.position)
            travel_time = distance / 10  # 10 m/s speed
            
            logging.info(f"DEPARTING {current.name} -> {nxt.name} ({distance}m, {travel_time:.1f}s)")
            current.status = StationStatus.IN_TRANSIT
            return travel_time
        return None
    
    def get_route(self) -> List[str]:
        """Get full monorail route"""
        return list(self.stations.keys())
    
    def get_status(self) -> Dict:
        """Get system status"""
        return {
            "current_station": self.current_station,
            "next_station": self.next_station,
            "stations": {
                name: {
                    "name": s.name,
                    "position": s.position,
                    "status": s.status.value,
                    "passengers_waiting": s.passengers_waiting
                }
                for name, s in self.stations.items()
            },
            "is_running": self.is_running
        }

async def main():
    system = StationSystem()
    
    logging.info("Starting automated monorail sequence...")
    
    # Simulation: Full route
    route = system.get_route()
    
    for i in range(len(route) - 1):
        current = route[i]
        nxt = route[i + 1]
        
        # Arrive at current station
        await system.arrive_at_station(current)
        
        # Board passengers
        await system.board_passengers(current, 10)
        
        # Depart to next station
        travel_time = await system.depart_from_station(current, nxt)
        
        # Simulate travel
        await asyncio.sleep(min(travel_time, 5))
    
    # Final station
    await system.arrive_at_station(route[-1])
    await system.board_passengers(route[-1], 5)
    
    logging.info("Route complete!")
    logging.info(json.dumps(system.get_status(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())

