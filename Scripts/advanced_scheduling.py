#!/usr/bin/env python3
"""
Advanced Scheduling & Route Optimization
Timetables, route planning, and optimization
"""

import logging
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

class MonorailLine(Enum):
    RESORT = "resort"
    EXPRESS = "express"
    EPCOT = "epcot"

@dataclass
class Station:
    """Station configuration"""
    id: str
    name: str
    position: float  # Distance from TTC in feet
    dwell_time: int  # Time to stop in seconds
    lines: List[MonorailLine] = field(default_factory=list)

@dataclass
class Route:
    """Optimized route"""
    train_id: str
    line: MonorailLine
    stations: List[Station]
    estimated_time: int  # Total time in seconds
    distance: float  # Total distance in feet

class ScheduleOptimizer:
    """Optimize monorail schedules and routes"""

    def __init__(self):
        self.stations = self._setup_stations()
        self.routes: Dict[str, List[Route]] = {}
        self.schedules: Dict[str, List[Dict]] = {}
        self.optimize_routes()

    def _setup_stations(self) -> Dict[str, Station]:
        """Configure all monorail stations"""
        return {
            "ttr": Station(
                "ttr", "Transportation & Ticket Center", 0, 30,
                [MonorailLine.RESORT, MonorailLine.EXPRESS, MonorailLine.EPCOT]
            ),
            "mk": Station(
                "mk", "Magic Kingdom", 1200, 45,
                [MonorailLine.RESORT, MonorailLine.EXPRESS]
            ),
            "gf": Station(
                "gf", "Grand Floridian Resort", 800, 30,
                [MonorailLine.RESORT]
            ),
            "pk": Station(
                "pk", "Polynesian Resort", 600, 25,
                [MonorailLine.RESORT]
            ),
            "epcot": Station(
                "epcot", "Epcot", 2400, 45,
                [MonorailLine.EXPRESS, MonorailLine.EPCOT]
            ),
            "hs": Station(
                "hs", "Hollywood Studios", 3000, 40,
                [MonorailLine.EXPRESS]
            ),
        }

    def optimize_routes(self):
        """Calculate optimal routes for each line"""
        # Resort Line: TTC → PK → GF → MK → TTC
        resort_route = Route(
            train_id="resort_line",
            line=MonorailLine.RESORT,
            stations=[
                self.stations["ttr"],
                self.stations["pk"],
                self.stations["gf"],
                self.stations["mk"],
                self.stations["ttr"]
            ],
            estimated_time=1800,
            distance=4400
        )

        # Express Line: TTC → MK → EPCOT → HS → TTC
        express_route = Route(
            train_id="express_line",
            line=MonorailLine.EXPRESS,
            stations=[
                self.stations["ttr"],
                self.stations["mk"],
                self.stations["epcot"],
                self.stations["hs"],
                self.stations["ttr"]
            ],
            estimated_time=2400,
            distance=6400
        )

        # Express to Epcot: TTC ↔ EPCOT (direct)
        epcot_route = Route(
            train_id="epcot_line",
            line=MonorailLine.EPCOT,
            stations=[
                self.stations["ttr"],
                self.stations["epcot"],
                self.stations["ttr"]
            ],
            estimated_time=900,
            distance=2400
        )

        self.routes[MonorailLine.RESORT.value] = [resort_route]
        self.routes[MonorailLine.EXPRESS.value] = [express_route]
        self.routes[MonorailLine.EPCOT.value] = [epcot_route]

        logging.info(f"Optimized {len(self.routes)} monorail routes")

    def generate_timetable(self, line: MonorailLine, start_hour: int, end_hour: int,
                          interval_minutes: int = 10) -> List[Dict]:
        """Generate timetable for a monorail line"""
        timetable = []
        current_time = datetime.now().replace(
            hour=start_hour, minute=0, second=0, microsecond=0
        )
        end_time = datetime.now().replace(
            hour=end_hour, minute=0, second=0, microsecond=0
        )

        train_number = 1
        while current_time < end_time:
            departure = current_time
            route = self.routes[line.value][0]
            arrival = departure + timedelta(seconds=route.estimated_time)

            timetable.append({
                "train_number": train_number,
                "line": line.value,
                "departure": departure.strftime("%H:%M"),
                "arrival": arrival.strftime("%H:%M"),
                "duration_minutes": int(route.estimated_time / 60),
                "distance_feet": route.distance,
                "status": "scheduled"
            })

            current_time += timedelta(minutes=interval_minutes)
            train_number += 1

        return timetable

    def calculate_shortest_path(self, start_station: str, end_station: str) -> Tuple[List[str], float]:
        """Dijkstra's algorithm to find shortest path between stations"""

        distances = {station_id: float('inf') for station_id in self.stations}
        distances[start_station] = 0
        previous = {}
        unvisited = set(self.stations.keys())

        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])
            if distances[current] == float('inf'):
                break

            if current == end_station:
                path = []
                node = end_station
                while node in previous:
                    path.insert(0, node)
                    node = previous[node]
                path.insert(0, start_station)
                return path, distances[end_station]

            unvisited.remove(current)

            for station_id, station in self.stations.items():
                if station_id in unvisited:
                    dist = abs(station.position - self.stations[current].position) / 5280
                    if distances[current] + dist < distances[station_id]:
                        distances[station_id] = distances[current] + dist
                        previous[station_id] = current

        return [], float('inf')

    def estimate_wait_time(self, station_id: str, line: MonorailLine) -> int:
        """Estimate passenger wait time at a station"""

        interval_minutes = 10
        return interval_minutes // 2

    def get_route_info(self, line: MonorailLine) -> Dict:
        """Get detailed route information"""

        route = self.routes[line.value][0]
        return {
            "line": line.value,
            "total_distance": f"{route.distance} feet ({route.distance/5280:.1f} miles)",
            "estimated_time": f"{route.estimated_time // 60} minutes",
            "stations": [
                {
                    "name": station.name,
                    "position": f"{station.position} feet",
                    "dwell_time": f"{station.dwell_time} seconds"
                }
                for station in route.stations
            ]
        }

async def demo_scheduling():
    """Demo advanced scheduling"""

    logging.info("=" * 70)
    logging.info("WDW Monorail - Advanced Scheduling & Optimization")
    logging.info("=" * 70)

    optimizer = ScheduleOptimizer()

    logging.info("\n📅 Generating timetables...")
    for line in MonorailLine:
        timetable = optimizer.generate_timetable(line, 9, 17, interval_minutes=10)
        logging.info(f"\n{line.value.upper()} Line Schedule:")
        for entry in timetable[:3]:
            logging.info(f"  Train {entry['train_number']:02d}: {entry['departure']} → {entry['arrival']} ({entry['duration_minutes']}m)")
        logging.info(f"  ... ({len(timetable)} trains total)")

    logging.info("\n🗺️ Route Information:")
    for line in MonorailLine:
        info = optimizer.get_route_info(line)
        logging.info(f"\n{line.value.upper()} Line:")
        logging.info(f"  Distance: {info['total_distance']}")
        logging.info(f"  Time: {info['estimated_time']}")
        logging.info(f"  Stations: {', '.join([s['name'] for s in info['stations']])}")

    logging.info("\n⏱️ Estimated Wait Times:")
    logging.info(f"  Magic Kingdom (Resort): ~{optimizer.estimate_wait_time('mk', MonorailLine.RESORT)} min")
    logging.info(f"  Epcot (Express): ~{optimizer.estimate_wait_time('epcot', MonorailLine.EXPRESS)} min")
    logging.info(f"  Hollywood Studios (Express): ~{optimizer.estimate_wait_time('hs', MonorailLine.EXPRESS)} min")

    logging.info("\n🧭 Route Planning:")
    path, distance = optimizer.calculate_shortest_path("ttr", "hs")
    logging.info(f"  TTC → Hollywood Studios: {' → '.join(path)}")
    logging.info(f"  Shortest distance: {distance:.1f} miles")

    logging.info("\n" + "=" * 70)
    logging.info("✅ Scheduling optimization demo complete!")
    logging.info("=" * 70)

if __name__ == "__main__":
    asyncio.run(demo_scheduling())













