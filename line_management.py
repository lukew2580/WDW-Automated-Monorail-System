#!/usr/bin/env python3
"""
WDW Monorail Line Management System
Handles Resort Line, Express Line, and Express to Epcot line routing
"""

import asyncio
import logging
from enum import Enum
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class MonorailLine(Enum):
    """WDW Monorail Lines"""
    RESORT_LINE = "resort"           # Magic Kingdom loop + resorts
    EXPRESS_LINE = "express"         # Direct MK to TTC
    EXPRESS_EPCOT = "express_epcot"  # TTC to Epcot only


class LineStation(Enum):
    """Stations on each line"""
    # All lines
    TICKET_CENTER = "ttr"
    MAGIC_KINGDOM = "mk"
    
    # Resort Line only
    GRAND_FLORIDIAN = "grand_floridian"
    POLYNESIAN = "polynesian"
    CONTEMPORARY = "contemporary"
    
    # Express to Epcot only
    EPCOT = "epcot"


@dataclass
class LineRoute:
    """Route definition for a monorail line"""
    line: MonorailLine
    name: str
    stations: List[LineStation]
    total_distance: float  # meters
    description: str
    color: str  # for UI


class LineManager:
    """Manages WDW monorail lines and routing"""
    
    def __init__(self):
        self.lines = self._define_lines()
        self.current_line: Optional[MonorailLine] = None
        self.line_history = []
        
    def _define_lines(self) -> Dict[MonorailLine, LineRoute]:
        """Define the three WDW monorail lines with stations and distances"""
        
        lines = {
            MonorailLine.RESORT_LINE: LineRoute(
                line=MonorailLine.RESORT_LINE,
                name="Resort Line",
                stations=[
                    LineStation.TICKET_CENTER,      # 0m
                    LineStation.GRAND_FLORIDIAN,    # ~2200m
                    LineStation.POLYNESIAN,          # ~4400m
                    LineStation.CONTEMPORARY,        # ~6600m
                    LineStation.MAGIC_KINGDOM,       # ~9000m
                    LineStation.TICKET_CENTER,      # ~11000m (loop back)
                ],
                total_distance=11000,
                description="Full loop: TTC → Grand Floridian → Polynesian → Contemporary → Magic Kingdom → TTC",
                color="#FF0000"  # Red
            ),
            
            MonorailLine.EXPRESS_LINE: LineRoute(
                line=MonorailLine.EXPRESS_LINE,
                name="Express Line",
                stations=[
                    LineStation.TICKET_CENTER,      # 0m
                    LineStation.MAGIC_KINGDOM,      # ~7000m direct
                    LineStation.TICKET_CENTER,      # ~14000m return
                ],
                total_distance=14000,
                description="Express: TTC ↔ Magic Kingdom (no resort stops)",
                color="#0000FF"  # Blue
            ),
            
            MonorailLine.EXPRESS_EPCOT: LineRoute(
                line=MonorailLine.EXPRESS_EPCOT,
                name="Express to Epcot",
                stations=[
                    LineStation.TICKET_CENTER,      # 0m
                    LineStation.EPCOT,              # ~6000m
                    LineStation.TICKET_CENTER,      # ~12000m return
                ],
                total_distance=12000,
                description="Express: TTC ↔ Epcot (direct line)",
                color="#FFB81C"  # Gold/Yellow
            ),
        }
        
        return lines
    
    def get_line_info(self, line: MonorailLine) -> LineRoute:
        """Get information about a specific line"""
        return self.lines[line]
    
    def get_stations_for_line(self, line: MonorailLine) -> List[LineStation]:
        """Get all stations on a specific line"""
        return self.lines[line].stations
    
    def get_next_station(self, current_line: MonorailLine, current_station: LineStation) -> Optional[LineStation]:
        """Get the next station on the current line"""
        stations = self.get_stations_for_line(current_line)
        try:
            current_idx = stations.index(current_station)
            # Return next station, or loop back to first if at end
            return stations[(current_idx + 1) % len(stations)]
        except ValueError:
            logger.warning(f"Station {current_station} not on line {current_line}")
            return None
    
    def get_distance_to_station(self, current_line: MonorailLine, 
                               current_station: LineStation, 
                               target_station: LineStation) -> Optional[float]:
        """Calculate distance between two stations on same line"""
        stations = self.get_stations_for_line(current_line)
        
        try:
            current_idx = stations.index(current_station)
            target_idx = stations.index(target_station)
        except ValueError:
            return None
        
        # Simple distance calculation based on station order
        total_distance = self.lines[current_line].total_distance
        station_count = len(stations)
        distance_per_segment = total_distance / station_count
        
        # Calculate forward distance
        if target_idx >= current_idx:
            distance = (target_idx - current_idx) * distance_per_segment
        else:
            # Loop around
            distance = (station_count - current_idx + target_idx) * distance_per_segment
        
        return distance


class MonorailLineTracker:
    """Tracks which line a monorail is on and manages line-specific behavior"""
    
    def __init__(self, monorail_id: str):
        self.monorail_id = monorail_id
        self.line_manager = LineManager()
        self.current_line: Optional[MonorailLine] = None
        self.current_station: Optional[LineStation] = None
        self.is_valid_on_line = False
        self.line_switch_count = 0
        self.last_line_check = datetime.now()
        
    async def identify_line(self, detected_stations: List[LineStation]) -> MonorailLine:
        """
        Identify which line the monorail is on based on detected stations
        """
        logger.info(f"[{self.monorail_id}] Identifying line from stations: {detected_stations}")
        
        # Check each line to see if detected stations match
        for line, route in self.line_manager.lines.items():
            matching_stations = [s for s in detected_stations if s in route.stations]
            match_percentage = len(matching_stations) / len(detected_stations) if detected_stations else 0
            
            if match_percentage >= 0.8:  # 80% match threshold
                logger.info(f"[{self.monorail_id}] Identified as {line.value.upper()}")
                self.current_line = line
                self.is_valid_on_line = True
                return line
        
        logger.warning(f"[{self.monorail_id}] Could not identify line from stations")
        self.is_valid_on_line = False
        return None
    
    async def set_line(self, line: MonorailLine, validate: bool = True) -> bool:
        """
        Manually set the line for this monorail
        """
        if validate and line not in self.line_manager.lines:
            logger.error(f"[{self.monorail_id}] Invalid line: {line}")
            return False
        
        old_line = self.current_line
        self.current_line = line
        self.is_valid_on_line = True
        self.line_switch_count += 1
        
        logger.info(f"[{self.monorail_id}] Line changed: {old_line} → {line.value.upper()}")
        logger.info(f"[{self.monorail_id}] Route: {self.line_manager.get_line_info(line).description}")
        
        return True
    
    async def update_station(self, station: LineStation) -> bool:
        """Update current station and validate it's on the current line"""
        if not self.current_line:
            logger.warning(f"[{self.monorail_id}] No line assigned yet")
            return False
        
        valid_stations = self.line_manager.get_stations_for_line(self.current_line)
        
        if station not in valid_stations:
            logger.warning(f"[{self.monorail_id}] Station {station} not on {self.current_line.value}")
            return False
        
        self.current_station = station
        logger.info(f"[{self.monorail_id}] At station: {station.value} on {self.current_line.value.upper()}")
        return True
    
    def get_line_status(self) -> Dict:
        """Get current line status"""
        if not self.current_line:
            return {"status": "no_line_assigned"}
        
        route = self.line_manager.get_line_info(self.current_line)
        next_station = self.line_manager.get_next_station(self.current_line, self.current_station) if self.current_station else None
        
        return {
            "monorail_id": self.monorail_id,
            "line": self.current_line.value,
            "line_name": route.name,
            "line_color": route.color,
            "current_station": self.current_station.value if self.current_station else None,
            "next_station": next_station.value if next_station else None,
            "route_description": route.description,
            "is_valid": self.is_valid_on_line,
            "total_route_distance": route.total_distance,
            "line_switches": self.line_switch_count,
        }


async def demo_line_management():
    """Demo line management system"""
    
    logger.info("="*70)
    logger.info("WDW MONORAIL LINE MANAGEMENT SYSTEM - DEMO")
    logger.info("="*70)
    logger.info("")
    
    # Create trackers for multiple monorails
    mk_train = MonorailLineTracker("monorail-mk-1")
    express_train = MonorailLineTracker("monorail-express-1")
    epcot_train = MonorailLineTracker("monorail-epcot-1")
    
    # Scenario 1: Magic Kingdom train on Resort Line
    logger.info("\n>>> SCENARIO 1: Magic Kingdom Resort Line Train")
    await mk_train.set_line(MonorailLine.RESORT_LINE)
    await mk_train.update_station(LineStation.TICKET_CENTER)
    await mk_train.update_station(LineStation.GRAND_FLORIDIAN)
    await mk_train.update_station(LineStation.POLYNESIAN)
    logger.info(f"Status: {mk_train.get_line_status()}")
    
    # Scenario 2: Express Line train
    logger.info("\n>>> SCENARIO 2: Express Line Train (TTC ↔ MK Direct)")
    await express_train.set_line(MonorailLine.EXPRESS_LINE)
    await express_train.update_station(LineStation.TICKET_CENTER)
    await express_train.update_station(LineStation.MAGIC_KINGDOM)
    logger.info(f"Status: {express_train.get_line_status()}")
    
    # Scenario 3: Epcot Express train
    logger.info("\n>>> SCENARIO 3: Express to Epcot Train")
    await epcot_train.set_line(MonorailLine.EXPRESS_EPCOT)
    await epcot_train.update_station(LineStation.TICKET_CENTER)
    await epcot_train.update_station(LineStation.EPCOT)
    logger.info(f"Status: {epcot_train.get_line_status()}")
    
    # Scenario 4: Auto-identify line from stations
    logger.info("\n>>> SCENARIO 4: Auto-Identify Line from Station Data")
    mystery_train = MonorailLineTracker("monorail-unknown")
    detected = [LineStation.TICKET_CENTER, LineStation.EPCOT]
    identified_line = await mystery_train.identify_line(detected)
    logger.info(f"Identified line: {identified_line.value.upper() if identified_line else 'UNKNOWN'}")
    
    # Show line info
    logger.info("\n>>> WDW MONORAIL LINES OVERVIEW")
    manager = LineManager()
    for line in MonorailLine:
        route = manager.get_line_info(line)
        logger.info(f"\n{route.name} ({line.value.upper()})")
        logger.info(f"  Color: {route.color}")
        logger.info(f"  Distance: {route.total_distance}m")
        logger.info(f"  Route: {route.description}")
        logger.info(f"  Stations: {', '.join([s.value for s in route.stations])}")
    
    logger.info("\n" + "="*70)
    logger.info("✅ Line management demo complete!")
    logger.info("="*70)


if __name__ == "__main__":
    asyncio.run(demo_line_management())

