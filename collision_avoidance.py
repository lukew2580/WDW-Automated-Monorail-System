#!/usr/bin/env python3
"""
Collision Avoidance System
Real-time track occupancy detection and conflict resolution
"""

import logging
import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

class SafetyLevel(Enum):
    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"
    COLLISION_IMMINENT = "collision_imminent"

@dataclass
class TrainPosition:
    """Train position data"""
    train_id: str
    line: str
    position: float  # Position in feet along track
    speed: float  # Speed in mph
    direction: str  # forward, reverse, stopped
    timestamp: float

@dataclass
class TrackSegment:
    """Track segment for occupancy tracking"""
    segment_id: str
    start_position: float
    end_position: float
    line: str
    occupying_trains: Set[str] = field(default_factory=set)
    last_update: float = 0

class CollisionAvoidanceSystem:
    """Prevent collisions through real-time monitoring"""
    
    # Safety parameters
    SAFE_DISTANCE = 500  # Minimum distance between trains in feet
    WARNING_DISTANCE = 1000  # Distance to start warning
    CRITICAL_DISTANCE = 200  # Critical safety distance
    REACTION_TIME = 2.0  # Seconds to react
    
    def __init__(self, track_length: float = 10000):
        self.track_length = track_length
        self.train_positions: Dict[str, TrainPosition] = {}
        self.track_segments = self._initialize_track_segments()
        self.collision_history: List[Dict] = []
        self.active_warnings: Set[str] = set()
        self.emergency_stops: Set[str] = set()
    
    def _initialize_track_segments(self) -> List[TrackSegment]:
        """Create track segments for occupancy tracking"""
        segments = []
        segment_length = 500  # 500 feet per segment
        segment_id = 0
        
        for start in range(0, int(self.track_length), segment_length):
            segments.append(TrackSegment(
                segment_id=f"segment_{segment_id}",
                start_position=start,
                end_position=min(start + segment_length, self.track_length),
                line="main"  # Simplified
            ))
            segment_id += 1
        
        logging.info(f"Track divided into {len(segments)} segments")
        return segments
    
    def update_train_position(self, train_id: str, position: float, speed: float, 
                            direction: str, line: str) -> SafetyLevel:
        """Update train position and check for collisions"""
        current_time = asyncio.get_event_loop().time()
        
        # Update train position
        self.train_positions[train_id] = TrainPosition(
            train_id=train_id,
            line=line,
            position=position,
            speed=speed,
            direction=direction,
            timestamp=current_time
        )
        
        # Update track occupancy
        self._update_track_occupancy(train_id, position)
        
        # Check for collisions
        safety_level = self._check_collision_risk(train_id)
        
        return safety_level
    
    def _update_track_occupancy(self, train_id: str, position: float):
        """Update which segments are occupied"""
        for segment in self.track_segments:
            if segment.start_position <= position <= segment.end_position:
                segment.occupying_trains.add(train_id)
                segment.last_update = asyncio.get_event_loop().time()
            else:
                segment.occupying_trains.discard(train_id)
    
    def _check_collision_risk(self, train_id: str) -> SafetyLevel:
        """Check for collision risk with other trains"""
        if train_id not in self.train_positions:
            return SafetyLevel.SAFE
        
        train = self.train_positions[train_id]
        min_distance = float('inf')
        closest_train = None
        
        # Check distance to all other trains on same line
        for other_id, other_train in self.train_positions.items():
            if other_id == train_id or other_train.line != train.line:
                continue
            
            distance = abs(train.position - other_train.position)
            
            if distance < min_distance:
                min_distance = distance
                closest_train = other_id
        
        # Determine safety level
        if min_distance < self.CRITICAL_DISTANCE:
            logging.critical(f"⚠️ COLLISION IMMINENT: {train_id} vs {closest_train} ({min_distance:.1f}ft)")
            self.emergency_stops.add(train_id)
            self.emergency_stops.add(closest_train)
            return SafetyLevel.COLLISION_IMMINENT
        
        elif min_distance < self.SAFE_DISTANCE:
            warning_id = f"{train_id}_{closest_train}"
            if warning_id not in self.active_warnings:
                logging.warning(f"⚠️ WARNING: {train_id} approaching {closest_train} ({min_distance:.1f}ft)")
                self.active_warnings.add(warning_id)
            return SafetyLevel.CRITICAL
        
        elif min_distance < self.WARNING_DISTANCE:
            warning_id = f"{train_id}_{closest_train}"
            if warning_id not in self.active_warnings:
                logging.warning(f"⚠️ CAUTION: {train_id} near {closest_train} ({min_distance:.1f}ft)")
                self.active_warnings.add(warning_id)
            return SafetyLevel.WARNING
        
        else:
            # Clear warning if trains are far apart
            self.active_warnings.discard(f"{train_id}_{closest_train}")
            return SafetyLevel.SAFE
    
    async def autonomous_speed_control(self, train_id: str) -> float:
        """Calculate safe speed based on obstacles ahead"""
        if train_id not in self.train_positions:
            return 0
        
        train = self.train_positions[train_id]
        safety_level = self._check_collision_risk(train_id)
        
        # Speed recommendations based on safety
        speed_limits = {
            SafetyLevel.SAFE: 35.0,  # Normal operating speed
            SafetyLevel.WARNING: 25.0,  # Slow down
            SafetyLevel.CRITICAL: 10.0,  # Very slow
            SafetyLevel.COLLISION_IMMINENT: 0.0,  # Emergency stop
        }
        
        recommended_speed = speed_limits[safety_level]
        
        if recommended_speed < train.speed:
            logging.info(f"Speed reduction: {train_id} {train.speed}mph → {recommended_speed}mph ({safety_level.value})")
        
        return recommended_speed
    
    async def emergency_stop_all(self):
        """Stop all trains immediately"""
        logging.critical("🛑 EMERGENCY STOP - ALL TRAINS")
        for train_id in self.train_positions.keys():
            self.emergency_stops.add(train_id)
        return True
    
    def get_safety_report(self) -> Dict:
        """Generate safety status report"""
        return {
            "total_trains": len(self.train_positions),
            "emergency_stops_active": list(self.emergency_stops),
            "active_warnings": list(self.active_warnings),
            "train_positions": [
                {
                    "train_id": train.train_id,
                    "position": f"{train.position:.1f} ft",
                    "speed": f"{train.speed:.1f} mph",
                    "line": train.line,
                    "direction": train.direction
                }
                for train in self.train_positions.values()
            ],
            "collision_history": self.collision_history
        }
    
    def get_occupancy_map(self) -> Dict[str, List[str]]:
        """Get track occupancy visualization"""
        return {
            segment.segment_id: list(segment.occupying_trains)
            for segment in self.track_segments
            if segment.occupying_trains
        }

async def demo_collision_avoidance():
    """Demo collision avoidance system"""
    logging.info("=" * 70)
    logging.info("WDW Monorail - Collision Avoidance System")
    logging.info("=" * 70)
    
    cas = CollisionAvoidanceSystem()
    
    # Scenario 1: Safe operation
    logging.info("\n✓ Scenario 1: Safe Operation")
    cas.update_train_position("monorail_red", 1000, 30, "forward", "resort")
    cas.update_train_position("monorail_orange", 4000, 30, "forward", "resort")
    safety = cas.update_train_position("monorail_yellow", 7000, 30, "forward", "resort")
    logging.info(f"  Safety Level: {safety.value}")
    
    # Scenario 2: Warning distance
    logging.info("\n⚠️ Scenario 2: Approaching Warning Distance")
    cas.update_train_position("monorail_red", 1500, 35, "forward", "express")
    safety = cas.update_train_position("monorail_orange", 2200, 30, "forward", "express")
    logging.info(f"  Safety Level: {safety.value}")
    
    # Scenario 3: Critical distance
    logging.info("\n🔴 Scenario 3: Critical Distance")
    cas.update_train_position("monorail_green", 3000, 30, "forward", "epcot")
    safety = cas.update_train_position("monorail_blue", 3150, 25, "forward", "epcot")
    logging.info(f"  Safety Level: {safety.value}")
    recommended_speed = await cas.autonomous_speed_control("monorail_blue")
    logging.info(f"  Recommended Speed: {recommended_speed} mph")
    
    # Scenario 4: Collision imminent
    logging.info("\n🚨 Scenario 4: Collision Imminent")
    cas.update_train_position("monorail_pink", 5000, 30, "forward", "express")
    safety = cas.update_train_position("monorail_coral", 5100, 32, "forward", "express")
    logging.info(f"  Safety Level: {safety.value}")
    
    # Safety report
    logging.info("\n📊 Safety Report:")
    report = cas.get_safety_report()
    logging.info(f"  Total Trains: {report['total_trains']}")
    logging.info(f"  Emergency Stops: {len(report['emergency_stops_active'])}")
    logging.info(f"  Active Warnings: {len(report['active_warnings'])}")
    
    # Occupancy map
    logging.info("\n🗺️ Track Occupancy:")
    occupancy = cas.get_occupancy_map()
    for segment, trains in list(occupancy.items())[:5]:
        logging.info(f"  {segment}: {', '.join(trains)}")
    
    logging.info("\n" + "=" * 70)
    logging.info("✅ Collision avoidance demo complete!")
    logging.info("=" * 70)

if __name__ == "__main__":
    asyncio.run(demo_collision_avoidance())

