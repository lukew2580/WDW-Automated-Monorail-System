#!/usr/bin/env python3
"""
Comprehensive Integration of Motor, Actuator, and Mesh Network
Demonstrates seamless operation of all components in the WDW Monorail System
"""

import asyncio
import logging
from typing import Dict, List
from motor_actuator_integration import MotorActuatorController, MeshNetworkMotorActuatorIntegration, MotorSpec, ActuatorSpec
from bluetooth_mesh import MonorailMeshNetwork, MonorailMeshNode, SwitchStation

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class ComprehensiveIntegration:
    """Integrates motor, actuator, and mesh network components"""
    
    def __init__(self):
        self.motor_controller = MotorActuatorController()
        self.mesh_network = MonorailMeshNetwork()
        self.mesh_integration = MeshNetworkMotorActuatorIntegration(self.motor_controller, self.mesh_network)
        
    def add_motor(self, motor_spec: MotorSpec):
        """Add a motor to the system"""
        self.motor_controller.add_motor(motor_spec)
        logger.info(f"Added motor {motor_spec.motor_id} with {len(motor_spec.compatible_actuators)} compatible actuators")
    
    def add_actuator(self, actuator_spec: ActuatorSpec):
        """Add an actuator to the system"""
        self.motor_controller.add_actuator(actuator_spec)
        logger.info(f"Added actuator {actuator_spec.actuator_id} with {len(actuator_spec.compatible_motors)} compatible motors")
    
    def add_monorail(self, monorail_id: str, bluetooth_address: str):
        """Add a monorail to the mesh network"""
        self.mesh_network.add_monorail(monorail_id, bluetooth_address)
        logger.info(f"Added monorail {monorail_id} to mesh network")
    
    def add_switch(self, station_id: str, position: float, switch_type: str = "motor"):
        """Add a switch station to the mesh network"""
        self.mesh_network.add_switch(station_id, position, switch_type)
        logger.info(f"Added {switch_type} switch {station_id} at position {position}m")
    
    async def sync_motor_actuator_status(self, motor_id: str, actuator_id: str, mesh_node_id: str):
        """Synchronize motor and actuator status with mesh network"""
        await self.mesh_integration.sync_motor_actuator_status(motor_id, actuator_id, mesh_node_id)
        logger.info(f"Synchronized {motor_id} and {actuator_id} status with mesh node {mesh_node_id}")
    
    async def check_collision_risk(self, monorail_id: str, next_position: float) -> bool:
        """Check if monorail moving to next_position would collide"""
        is_collision = await self.mesh_network.check_collision_risk(monorail_id, next_position)
        logger.info(f"Collision risk for {monorail_id} at {next_position}m: {is_collision}")
        return is_collision
    
    async def handle_switch_passage(self, monorail_id: str, switch_id: str, incoming_route: str) -> bool:
        """Coordinate monorail passage through switch"""
        can_pass = await self.mesh_network.handle_switch_passage(monorail_id, switch_id, incoming_route)
        logger.info(f"Monorail {monorail_id} can pass through {switch_id}: {can_pass}")
        return can_pass
    
    async def run_comprehensive_test(self):
        """Run a comprehensive test of all integrated components"""
        logger.info("\n=== Running Comprehensive Integration Test ===\n")
        
        # Add motors and actuators
        self.add_motor(MotorSpec(
            motor_id="motor_track_1",
            motor_type="High-Torque Electric",
            power_rating=5.0,
            torque=100.0,
            control_interface="PLC",
            compatible_actuators=["actuator_track_1", "actuator_track_2"]
        ))
        
        self.add_motor(MotorSpec(
            motor_id="motor_monorail_1",
            motor_type="Precision Electric",
            power_rating=3.0,
            torque=75.0,
            control_interface="Direct",
            compatible_actuators=["actuator_monorail_1", "actuator_monorail_2"]
        ))
        
        self.add_motor(MotorSpec(
            motor_id="motor_barn_1",
            motor_type="Precision Electric",
            power_rating=2.0,
            torque=50.0,
            control_interface="Mesh",
            compatible_actuators=["actuator_barn_1", "actuator_barn_2"]
        ))
        
        self.add_actuator(ActuatorSpec(
            actuator_id="actuator_track_1",
            actuator_type="Linear Actuator",
            stroke_length=500.0,
            force=1000.0,
            control_interface="PLC",
            compatible_motors=["motor_track_1", "motor_track_2"]
        ))
        
        self.add_actuator(ActuatorSpec(
            actuator_id="actuator_monorail_1",
            actuator_type="Rotary Actuator",
            stroke_length=360.0,
            force=800.0,
            control_interface="Direct",
            compatible_motors=["motor_monorail_1", "motor_monorail_2"]
        ))
        
        self.add_actuator(ActuatorSpec(
            actuator_id="actuator_barn_1",
            actuator_type="Linear Actuator",
            stroke_length=300.0,
            force=600.0,
            control_interface="Mesh",
            compatible_motors=["motor_barn_1", "motor_barn_2"]
        ))
        
        # Add monorails and switches
        self.add_monorail("monorail_1", "00:1A:7D:DA:71:13")
        self.add_monorail("monorail_2", "00:1A:7D:DA:71:14")
        
        self.add_switch("switch_main_branch", 5000, switch_type="motor")
        self.add_switch("switch_manual_divert", 8000, switch_type="manual")
        
        # Synchronize motor and actuator status
        await self.sync_motor_actuator_status("motor_track_1", "actuator_track_1", "monorail_1")
        await self.sync_motor_actuator_status("motor_monorail_1", "actuator_monorail_1", "monorail_2")
        
        # Check collision risk
        await self.check_collision_risk("monorail_1", 5050)
        await self.check_collision_risk("monorail_2", 5100)
        
        # Handle switch passage
        await self.handle_switch_passage("monorail_1", "switch_main_branch", "main")
        await self.handle_switch_passage("monorail_2", "switch_main_branch", "branch")
        
        # Simulate monorail movement
        monorail_1 = self.mesh_network.nodes["monorail_1"]
        monorail_2 = self.mesh_network.nodes["monorail_2"]
        
        monorail_1.position = 4900
        monorail_1.speed = 0.5
        monorail_1.is_moving = True
        monorail_1.next_station = "switch"
        
        monorail_2.position = 5100
        monorail_2.speed = 0.3
        monorail_2.is_moving = True
        monorail_2.next_station = "branch"
        
        # Broadcast status
        await self.mesh_network.broadcast_all_status()
        
        # Release switch passage
        await self.mesh_network.switches["switch_main_branch"].release_passage("monorail_1")
        
        # Manual switch override
        self.mesh_network.switches["switch_manual_divert"].set_manual_position("branch")
        
        logger.info("\n✅ Comprehensive integration test complete!")


async def main():
    """Run the comprehensive integration demo"""
    integration = ComprehensiveIntegration()
    await integration.run_comprehensive_test()


if __name__ == "__main__":
    asyncio.run(main())


