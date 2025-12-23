#!/usr/bin/env python3
"""
Bluetooth Mesh Network for WDW Monorails
Enables monorails to communicate position, status, and coordinate at switches
"""

import asyncio
import json
import logging
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime
import bleak
from bleak import BleakScanner, BleakClient

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

@dataclass
class MonorailStatus:
    """Status packet sent between monorails"""
    monorail_id: str
    position: float  # meters along track
    speed: float  # m/s
    is_moving: bool
    battery_percent: int
    timestamp: str
    next_station: str
    can_proceed: bool  # Can this monorail move forward?
    
    def to_json(self) -> str:
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, data: str) -> "MonorailStatus":
        return cls(**json.loads(data))


class MonorailMeshNode:
    """Individual monorail in the mesh network"""
    
    def __init__(self, monorail_id: str, bluetooth_address: str):
        self.monorail_id = monorail_id
        self.bluetooth_address = bluetooth_address
        self.position = 0.0
        self.speed = 0.0
        self.is_moving = False
        self.battery_percent = 100
        self.next_station = "depot"
        self.can_proceed = True
        self.last_update = datetime.now().isoformat()
        self.peers: Dict[str, MonorailStatus] = {}  # Other monorails we know about
        self.client: Optional[BleakClient] = None
        
    async def connect(self) -> bool:
        """Connect to this monorail via Bluetooth"""
        try:
            self.client = BleakClient(self.bluetooth_address)
            await self.client.connect()
            logger.info(f"[{self.monorail_id}] Connected via Bluetooth")
            return True
        except Exception as e:
            logger.error(f"[{self.monorail_id}] Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect Bluetooth"""
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            logger.info(f"[{self.monorail_id}] Disconnected")
    
    def get_status(self) -> MonorailStatus:
        """Get current status as packet"""
        return MonorailStatus(
            monorail_id=self.monorail_id,
            position=self.position,
            speed=self.speed,
            is_moving=self.is_moving,
            battery_percent=self.battery_percent,
            timestamp=datetime.now().isoformat(),
            next_station=self.next_station,
            can_proceed=self.can_proceed
        )
    
    async def broadcast_status(self, peers: List["MonorailMeshNode"]):
        """Broadcast our status to all nearby peers"""
        status = self.get_status()
        status_json = status.to_json()
        
        for peer in peers:
            if peer.monorail_id != self.monorail_id and peer.client:
                try:
                    # Send status to peer (would use BLE characteristic write)
                    logger.info(f"[{self.monorail_id}] Broadcasting to {peer.monorail_id}: pos={self.position}m, moving={self.is_moving}")
                except Exception as e:
                    logger.error(f"Broadcast to {peer.monorail_id} failed: {e}")
    
    async def receive_status(self, status: MonorailStatus):
        """Receive status from peer monorail"""
        self.peers[status.monorail_id] = status
        logger.info(f"[{self.monorail_id}] Heard from {status.monorail_id}: pos={status.position}m, can_proceed={status.can_proceed}")


class SwitchStation:
    """Manual or motorized switch point where monorails coordinate"""
    
    def __init__(self, station_id: str, position: float, switch_type: str = "motor"):
        self.station_id = station_id
        self.position = position  # Position on main track
        self.switch_type = switch_type  # "motor" or "manual"
        self.current_route = "main"  # "main" or "branch"
        self.is_occupied = False
        self.occupying_monorail = None
        self.queue: List[str] = []  # Monorails waiting to cross
        self.manual_override = False  # If manual, this tracks if someone turned it
        
    def can_monorail_pass(self, monorail_id: str, incoming_route: str) -> bool:
        """Check if monorail can pass through switch"""
        if self.is_occupied and self.occupying_monorail != monorail_id:
            return False
        
        if incoming_route != self.current_route and self.is_occupied:
            return False
        
        return True
    
    async def request_passage(self, monorail_id: str, incoming_route: str) -> bool:
        """Monorail requests to pass through switch"""
        if self.can_monorail_pass(monorail_id, incoming_route):
            self.is_occupied = True
            self.occupying_monorail = monorail_id
            logger.info(f"[SWITCH {self.station_id}] {monorail_id} GRANTED passage on {incoming_route}")
            return True
        else:
            self.queue.append((monorail_id, incoming_route))
            logger.info(f"[SWITCH {self.station_id}] {monorail_id} QUEUED (occupied by {self.occupying_monorail})")
            return False
    
    async def release_passage(self, monorail_id: str):
        """Monorail exits switch"""
        if self.occupying_monorail == monorail_id:
            self.is_occupied = False
            self.occupying_monorail = None
            logger.info(f"[SWITCH {self.station_id}] {monorail_id} released switch")
            
            # Process queue
            if self.queue:
                next_monorail, next_route = self.queue.pop(0)
                logger.info(f"[SWITCH {self.station_id}] Granting {next_monorail} from queue")
    
    def set_manual_position(self, position: str):
        """Manual switch turned by hand"""
        if self.switch_type == "manual":
            self.current_route = position
            self.manual_override = True
            logger.info(f"[SWITCH {self.station_id}] Manual override: route set to {position}")


class MonorailMeshNetwork:
    """Central coordinator for all monorails in mesh"""
    
    def __init__(self):
        self.nodes: Dict[str, MonorailMeshNode] = {}
        self.switches: Dict[str, SwitchStation] = {}
        self.running = False
        
    def add_monorail(self, monorail_id: str, bluetooth_address: str):
        """Register a monorail in the network"""
        node = MonorailMeshNode(monorail_id, bluetooth_address)
        self.nodes[monorail_id] = node
        logger.info(f"Added monorail {monorail_id} to mesh network")
    
    def add_switch(self, station_id: str, position: float, switch_type: str = "motor"):
        """Register a switch station"""
        switch = SwitchStation(station_id, position, switch_type)
        self.switches[station_id] = switch
        logger.info(f"Added {switch_type} switch {station_id} at position {position}m")
    
    async def check_collision_risk(self, monorail_id: str, next_position: float) -> bool:
        """Check if monorail moving to next_position would collide"""
        node = self.nodes.get(monorail_id)
        if not node:
            return False
        
        collision_distance = 0.5  # 50cm safe distance
        
        for other_id, other_status in node.peers.items():
            if abs(other_status.position - next_position) < collision_distance:
                logger.warning(f"[{monorail_id}] Collision risk with {other_id} at {next_position}m!")
                return True
        
        return False
    
    async def handle_switch_passage(self, monorail_id: str, switch_id: str, incoming_route: str) -> bool:
        """Coordinate monorail passage through switch"""
        switch = self.switches.get(switch_id)
        if not switch:
            return False
        
        return await switch.request_passage(monorail_id, incoming_route)
    
    async def broadcast_all_status(self):
        """All monorails broadcast their status"""
        nodes_list = list(self.nodes.values())
        for node in nodes_list:
            await node.broadcast_status(nodes_list)
    
    async def run_mesh(self, interval: float = 2.0):
        """Run mesh network coordination loop"""
        self.running = True
        logger.info("Mesh network started")
        
        while self.running:
            try:
                await self.broadcast_all_status()
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Mesh loop error: {e}")
    
    def stop_mesh(self):
        """Stop mesh network"""
        self.running = False
        logger.info("Mesh network stopped")


# Example usage / testing
async def main():
    """Demo: Two monorails, one switch station"""
    mesh = MonorailMeshNetwork()
    
    # Add two monorails
    mesh.add_monorail("monorail-1", "00:1A:7D:DA:71:13")
    mesh.add_monorail("monorail-2", "00:1A:7D:DA:71:14")
    
    # Add a switch station (motorized at 5000m)
    mesh.add_switch("switch-main-branch", 5000, switch_type="motor")
    
    # Add a manual switch (at 8000m)
    mesh.add_switch("switch-manual-divert", 8000, switch_type="manual")
    
    # Simulate monorails moving
    node1 = mesh.nodes["monorail-1"]
    node2 = mesh.nodes["monorail-2"]
    
    node1.position = 4900
    node1.speed = 0.5
    node1.is_moving = True
    node1.next_station = "switch"
    
    node2.position = 5100
    node2.speed = 0.3
    node2.is_moving = True
    node2.next_station = "branch"
    
    # Simulate mesh communication
    logger.info("\n=== SIMULATING MESH NETWORK ===\n")
    
    # Broadcast positions
    await mesh.broadcast_all_status()
    
    # Monorail 1 requests switch passage
    can_pass = await mesh.handle_switch_passage("monorail-1", "switch-main-branch", "main")
    logger.info(f"Monorail 1 can pass: {can_pass}\n")
    
    # Monorail 2 requests (should be queued)
    can_pass = await mesh.handle_switch_passage("monorail-2", "switch-main-branch", "branch")
    logger.info(f"Monorail 2 can pass: {can_pass}\n")
    
    # Monorail 1 exits
    await mesh.switches["switch-main-branch"].release_passage("monorail-1")
    
    # Check collision risk
    is_collision = await mesh.check_collision_risk("monorail-1", 5050)
    logger.info(f"Collision risk at 5050m: {is_collision}\n")
    
    # Manual switch override
    mesh.switches["switch-manual-divert"].set_manual_position("branch")
    
    logger.info("\n✅ Mesh network demo complete!")


if __name__ == "__main__":
    asyncio.run(main())

