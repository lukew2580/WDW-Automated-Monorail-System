#!/usr/bin/env python3
"""
WDW Monorail Motor and Actuator Integration
Ensures compatibility and synchronization of motors and actuators with the mesh network
"""

import asyncio
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from bluetooth_mesh import MonorailMeshNode, MonorailStatus, MonorailMeshNetwork

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class MotorSpec:
    """Specifications for a motor"""
    motor_id: str
    motor_type: str
    power_rating: float  # in kW
    torque: float  # in Nm
    control_interface: str  # e.g., "PLC", "Direct", "Mesh"
    compatible_actuators: List[str]


@dataclass
class ActuatorSpec:
    """Specifications for an actuator"""
    actuator_id: str
    actuator_type: str
    stroke_length: float  # in mm
    force: float  # in N
    control_interface: str  # e.g., "PLC", "Direct", "Mesh"
    compatible_motors: List[str]


class MotorActuatorController:
    """Controls and integrates motors and actuators with the mesh network"""
    
    def __init__(self):
        self.motors: Dict[str, MotorSpec] = {}
        self.actuators: Dict[str, ActuatorSpec] = {}
        self.motor_actuator_mapping: Dict[str, List[str]] = {}  # Maps motors to compatible actuators
        self.actuator_motor_mapping: Dict[str, List[str]] = {}  # Maps actuators to compatible motors
        
    def add_motor(self, motor_spec: MotorSpec):
        """Add a motor to the controller"""
        self.motors[motor_spec.motor_id] = motor_spec
        self.motor_actuator_mapping[motor_spec.motor_id] = motor_spec.compatible_actuators
        logger.info(f"Added motor {motor_spec.motor_id} with {len(motor_spec.compatible_actuators)} compatible actuators")
        
    def add_actuator(self, actuator_spec: ActuatorSpec):
        """Add an actuator to the controller"""
        self.actuators[actuator_spec.actuator_id] = actuator_spec
        self.actuator_motor_mapping[actuator_spec.actuator_id] = actuator_spec.compatible_motors
        logger.info(f"Added actuator {actuator_spec.actuator_id} with {len(actuator_spec.compatible_motors)} compatible motors")
        
    def get_compatible_actuators(self, motor_id: str) -> List[str]:
        """Get actuators compatible with a specific motor"""
        return self.motor_actuator_mapping.get(motor_id, [])
        
    def get_compatible_motors(self, actuator_id: str) -> List[str]:
        """Get motors compatible with a specific actuator"""
        return self.actuator_motor_mapping.get(actuator_id, [])
        
    def check_compatibility(self, motor_id: str, actuator_id: str) -> bool:
        """Check if a motor and actuator are compatible"""
        compatible_actuators = self.get_compatible_actuators(motor_id)
        compatible_motors = self.get_compatible_motors(actuator_id)
        
        return actuator_id in compatible_actuators and motor_id in compatible_motors


class MeshNetworkMotorActuatorIntegration:
    """Integrates motor and actuator control with mesh network"""
    
    def __init__(self, motor_controller: MotorActuatorController, mesh_network: MonorailMeshNetwork):
        self.motor_controller = motor_controller
        self.mesh_network = mesh_network
        self.motor_mesh_mapping: Dict[str, str] = {}  # motor_id -> mesh_node_id
        self.actuator_mesh_mapping: Dict[str, str] = {}  # actuator_id -> mesh_node_id
        
    def add_motor_to_mesh(self, motor_id: str, mesh_node_id: str):
        """Map a motor to a mesh node"""
        self.motor_mesh_mapping[motor_id] = mesh_node_id
        logger.info(f"Mapped motor {motor_id} to mesh node {mesh_node_id}")
        
    def add_actuator_to_mesh(self, actuator_id: str, mesh_node_id: str):
        """Map an actuator to a mesh node"""
        self.actuator_mesh_mapping[actuator_id] = mesh_node_id
        logger.info(f"Mapped actuator {actuator_id} to mesh node {mesh_node_id}")
        
    async def sync_motor_actuator_status(self, motor_id: str, actuator_id: str, mesh_node_id: str):
        """Synchronize motor and actuator status with mesh network"""
        # Check if motor and actuator are compatible
        if not self.motor_controller.check_compatibility(motor_id, actuator_id):
            logger.error(f"Motor {motor_id} and actuator {actuator_id} are not compatible")
            return
        
        # Add motor and actuator to mesh network
        self.add_motor_to_mesh(motor_id, mesh_node_id)
        self.add_actuator_to_mesh(actuator_id, mesh_node_id)
        
        # Log synchronization
        logger.info(f"Synchronized {motor_id} and {actuator_id} status with mesh node {mesh_node_id}")
        
        # Broadcast status to mesh network
        if mesh_node_id in self.mesh_network.nodes:
            node = self.mesh_network.nodes[mesh_node_id]
            await node.broadcast_status(list(self.mesh_network.nodes.values()))
        
    async def check_collision_risk(self, monorail_id: str, next_position: float) -> bool:
        """Check if monorail moving to next_position would collide"""
        return await self.mesh_network.check_collision_risk(monorail_id, next_position)
        
    async def handle_switch_passage(self, monorail_id: str, switch_id: str, incoming_route: str) -> bool:
        """Coordinate monorail passage through switch"""
        return await self.mesh_network.handle_switch_passage(monorail_id, switch_id, incoming_route)


async def main():
    """Demo: Integrate motors and actuators with the mesh network"""
    # Initialize controllers
    motor_actuator_controller = MotorActuatorController()
    mesh_integration = MeshNetworkMotorActuatorIntegration(motor_actuator_controller)
    
    # Add motors
    motor_actuator_controller.add_motor(MotorSpec(
        motor_id="motor_track_1",
        motor_type="High-Torque Electric",
        power_rating=5.0,
        torque=100.0,
        control_interface="PLC",
        compatible_actuators=["actuator_switch_1", "actuator_switch_2"]
    ))
    
    motor_actuator_controller.add_motor(MotorSpec(
        motor_id="motor_monorail_1",
        motor_type="Precision Electric",
        power_rating=3.0,
        torque=75.0,
        control_interface="Direct",
        compatible_actuators=["actuator_monorail_1", "actuator_monorail_2"]
    ))
    
    motor_actuator_controller.add_motor(MotorSpec(
        motor_id="motor_barn_1",
        motor_type="Precision Electric",
        power_rating=2.0,
        torque=50.0,
        control_interface="Mesh",
        compatible_actuators=["actuator_barn_1", "actuator_barn_2"]
    ))
    
    # Add actuators
    motor_actuator_controller.add_actuator(ActuatorSpec(
        actuator_id="actuator_switch_1",
        actuator_type="Linear Actuator",
        stroke_length=500.0,
        force=1000.0,
        control_interface="PLC",
        compatible_motors=["motor_track_1", "motor_track_2"]
    ))
    
    motor_actuator_controller.add_actuator(ActuatorSpec(
        actuator_id="actuator_monorail_1",
        actuator_type="Rotary Actuator",
        stroke_length=360.0,
        force=800.0,
        control_interface="Direct",
        compatible_motors=["motor_monorail_1", "motor_monorail_2"]
    ))
    
    motor_actuator_controller.add_actuator(ActuatorSpec(
        actuator_id="actuator_barn_1",
        actuator_type="Linear Actuator",
        stroke_length=300.0,
        force=600.0,
        control_interface="Mesh",
        compatible_motors=["motor_barn_1", "motor_barn_2"]
    ))
    
    # Add mesh nodes
    mesh_node_1 = MonorailMeshNode("monorail_1", "00:1A:7D:DA:71:13")
    mesh_node_1.position = 1000.0
    mesh_node_1.speed = 0.5
    mesh_node_1.is_moving = True
    mesh_node_1.next_station = "switch_1"
    mesh_integration.add_mesh_node(mesh_node_1)
    
    mesh_node_2 = MonorailMeshNode("monorail_2", "00:1A:7D:DA:71:14")
    mesh_node_2.position = 1500.0
    mesh_node_2.speed = 0.3
    mesh_node_2.is_moving = True
    mesh_node_2.next_station = "switch_2"
    mesh_integration.add_mesh_node(mesh_node_2)
    
    # Sync motor and actuator status with mesh nodes
    await mesh_integration.sync_motor_actuator_status("motor_track_1", "actuator_switch_1", "monorail_1")
    await mesh_integration.sync_motor_actuator_status("motor_monorail_1", "actuator_monorail_1", "monorail_2")
    
    logger.info("\n✅ Motor and actuator integration demo complete!")


if __name__ == "__main__":
    asyncio.run(main())





