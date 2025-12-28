#!/usr/bin/env python3
"""
Test Script for Motor, Actuator, and Mesh Network Integration
Validates the compatibility and synchronization of all components
"""

import asyncio
import logging
from typing import Dict, List
from motor_actuator_integration import MotorActuatorController, MeshNetworkMotorActuatorIntegration, MotorSpec, ActuatorSpec
from bluetooth_mesh import MonorailMeshNode, MonorailMeshNetwork, SwitchStation

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class TestMotorActuatorMeshIntegration:
    """Test class for motor, actuator, and mesh network integration"""
    
    def __init__(self):
        self.motor_actuator_controller = MotorActuatorController()
        self.mesh_integration = MeshNetworkMotorActuatorIntegration(self.motor_actuator_controller)
        self.mesh_network = MonorailMeshNetwork()
        
    async def setup_test_environment(self):
        """Set up the test environment with motors, actuators, and mesh nodes"""
        # Add motors
        self.motor_actuator_controller.add_motor(MotorSpec(
            motor_id="motor_track_1",
            motor_type="High-Torque Electric",
            power_rating=5.0,
            torque=100.0,
            control_interface="PLC",
            compatible_actuators=["actuator_switch_1", "actuator_switch_2"]
        ))
        
        self.motor_actuator_controller.add_motor(MotorSpec(
            motor_id="motor_track_2",
            motor_type="High-Torque Electric",
            power_rating=5.0,
            torque=100.0,
            control_interface="PLC",
            compatible_actuators=["actuator_switch_1", "actuator_switch_2"]
        ))
        
        self.motor_actuator_controller.add_motor(MotorSpec(
            motor_id="motor_monorail_1",
            motor_type="Precision Electric",
            power_rating=3.0,
            torque=75.0,
            control_interface="Direct",
            compatible_actuators=["actuator_monorail_1", "actuator_monorail_2"]
        ))
        
        self.motor_actuator_controller.add_motor(MotorSpec(
            motor_id="motor_monorail_2",
            motor_type="Precision Electric",
            power_rating=3.0,
            torque=75.0,
            control_interface="Direct",
            compatible_actuators=["actuator_monorail_1", "actuator_monorail_2"]
        ))
        
        self.motor_actuator_controller.add_motor(MotorSpec(
            motor_id="motor_barn_1",
            motor_type="Precision Electric",
            power_rating=2.0,
            torque=50.0,
            control_interface="Mesh",
            compatible_actuators=["actuator_barn_1", "actuator_barn_2"]
        ))
        
        self.motor_actuator_controller.add_motor(MotorSpec(
            motor_id="motor_barn_2",
            motor_type="Precision Electric",
            power_rating=2.0,
            torque=50.0,
            control_interface="Mesh",
            compatible_actuators=["actuator_barn_1", "actuator_barn_2"]
        ))
        
        # Add actuators
        self.motor_actuator_controller.add_actuator(ActuatorSpec(
            actuator_id="actuator_switch_1",
            actuator_type="Linear Actuator",
            stroke_length=500.0,
            force=1000.0,
            control_interface="PLC",
            compatible_motors=["motor_track_1", "motor_track_2"]
        ))
        
        self.motor_actuator_controller.add_actuator(ActuatorSpec(
            actuator_id="actuator_switch_2",
            actuator_type="Linear Actuator",
            stroke_length=500.0,
            force=1000.0,
            control_interface="PLC",
            compatible_motors=["motor_track_1", "motor_track_2"]
        ))
        
        self.motor_actuator_controller.add_actuator(ActuatorSpec(
            actuator_id="actuator_monorail_1",
            actuator_type="Rotary Actuator",
            stroke_length=360.0,
            force=800.0,
            control_interface="Direct",
            compatible_motors=["motor_monorail_1", "motor_monorail_2"]
        ))
        
        self.motor_actuator_controller.add_actuator(ActuatorSpec(
            actuator_id="actuator_monorail_2",
            actuator_type="Rotary Actuator",
            stroke_length=360.0,
            force=800.0,
            control_interface="Direct",
            compatible_motors=["motor_monorail_1", "motor_monorail_2"]
        ))
        
        self.motor_actuator_controller.add_actuator(ActuatorSpec(
            actuator_id="actuator_barn_1",
            actuator_type="Linear Actuator",
            stroke_length=300.0,
            force=600.0,
            control_interface="Mesh",
            compatible_motors=["motor_barn_1", "motor_barn_2"]
        ))
        
        self.motor_actuator_controller.add_actuator(ActuatorSpec(
            actuator_id="actuator_barn_2",
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
        self.mesh_integration.add_mesh_node(mesh_node_1)
        self.mesh_network.add_monorail("monorail_1", "00:1A:7D:DA:71:13")
        
        mesh_node_2 = MonorailMeshNode("monorail_2", "00:1A:7D:DA:71:14")
        mesh_node_2.position = 1500.0
        mesh_node_2.speed = 0.3
        mesh_node_2.is_moving = True
        mesh_node_2.next_station = "switch_2"
        self.mesh_integration.add_mesh_node(mesh_node_2)
        self.mesh_network.add_monorail("monorail_2", "00:1A:7D:DA:71:14")
        
        # Add switch stations
        self.mesh_network.add_switch("switch_1", 1200.0, switch_type="motor")
        self.mesh_network.add_switch("switch_2", 1700.0, switch_type="motor")
        
    async def test_compatibility(self):
        """Test the compatibility of motors and actuators"""
        logger.info("\n=== Testing Motor and Actuator Compatibility ===")
        
        # Test compatible pairs
        compatible_pairs = [
            ("motor_track_1", "actuator_switch_1"),
            ("motor_track_2", "actuator_switch_2"),
            ("motor_monorail_1", "actuator_monorail_1"),
            ("motor_monorail_2", "actuator_monorail_2"),
            ("motor_barn_1", "actuator_barn_1"),
            ("motor_barn_2", "actuator_barn_2")
        ]
        
        for motor_id, actuator_id in compatible_pairs:
            is_compatible = self.motor_actuator_controller.check_compatibility(motor_id, actuator_id)
            logger.info(f"{motor_id} and {actuator_id}: {'Compatible' if is_compatible else 'Not Compatible'}")
            assert is_compatible, f"{motor_id} and {actuator_id} should be compatible"
        
        # Test incompatible pairs
        incompatible_pairs = [
            ("motor_track_1", "actuator_monorail_1"),
            ("motor_monorail_1", "actuator_switch_1"),
            ("motor_barn_1", "actuator_switch_1")
        ]
        
        for motor_id, actuator_id in incompatible_pairs:
            is_compatible = self.motor_actuator_controller.check_compatibility(motor_id, actuator_id)
            logger.info(f"{motor_id} and {actuator_id}: {'Compatible' if is_compatible else 'Not Compatible'}")
            assert not is_compatible, f"{motor_id} and {actuator_id} should not be compatible"
        
        logger.info("✅ Compatibility tests passed!")
        
    async def test_mesh_integration(self):
        """Test the integration of motors and actuators with the mesh network"""
        logger.info("\n=== Testing Mesh Network Integration ===")
        
        # Sync motor and actuator status with mesh nodes
        sync_tasks = [
            self.mesh_integration.sync_motor_actuator_status("motor_track_1", "actuator_switch_1", "monorail_1"),
            self.mesh_integration.sync_motor_actuator_status("motor_monorail_1", "actuator_monorail_1", "monorail_2"),
            self.mesh_integration.sync_motor_actuator_status("motor_barn_1", "actuator_barn_1", "monorail_1")
        ]
        
        results = await asyncio.gather(*sync_tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Sync failed: {result}")
                assert False, f"Sync failed: {result}"
            else:
                assert result, "Sync should return True"
        
        logger.info("✅ Mesh integration tests passed!")
        
    async def test_switch_coordination(self):
        """Test the coordination of monorails through switch stations"""
        logger.info("\n=== Testing Switch Coordination ===")
        
        # Monorail 1 requests passage through switch 1
        can_pass = await self.mesh_network.handle_switch_passage("monorail_1", "switch_1", "main")
        logger.info(f"Monorail 1 can pass switch 1: {can_pass}")
        assert can_pass, "Monorail 1 should be able to pass switch 1"
        
        # Monorail 2 requests passage through switch 1 (should be queued)
        can_pass = await self.mesh_network.handle_switch_passage("monorail_2", "switch_1", "branch")
        logger.info(f"Monorail 2 can pass switch 1: {can_pass}")
        assert not can_pass, "Monorail 2 should be queued at switch 1"
        
        # Monorail 1 exits switch 1
        await self.mesh_network.switches["switch_1"].release_passage("monorail_1")
        
        # Monorail 2 should now be able to pass switch 1
        can_pass = await self.mesh_network.handle_switch_passage("monorail_2", "switch_1", "branch")
        logger.info(f"Monorail 2 can pass switch 1 after release: {can_pass}")
        assert can_pass, "Monorail 2 should now be able to pass switch 1"
        
        logger.info("✅ Switch coordination tests passed!")
        
    async def test_collision_detection(self):
        """Test the collision detection mechanism"""
        logger.info("\n=== Testing Collision Detection ===")
        
        # Check collision risk for monorail 1
        is_collision = await self.mesh_network.check_collision_risk("monorail_1", 1250.0)
        logger.info(f"Collision risk for monorail 1 at 1250m: {is_collision}")
        assert not is_collision, "Monorail 1 should not have a collision risk at 1250m"
        
        # Check collision risk for monorail 2
        is_collision = await self.mesh_network.check_collision_risk("monorail_2", 1550.0)
        logger.info(f"Collision risk for monorail 2 at 1550m: {is_collision}")
        assert not is_collision, "Monorail 2 should not have a collision risk at 1550m"
        
        logger.info("✅ Collision detection tests passed!")
        
    async def run_all_tests(self):
        """Run all tests"""
        logger.info("\n=== Running All Tests ===")
        
        await self.setup_test_environment()
        await self.test_compatibility()
        await self.test_mesh_integration()
        await self.test_switch_coordination()
        await self.test_collision_detection()
        
        logger.info("\n✅ All tests passed!")


async def main():
    """Run the test suite"""
    test_suite = TestMotorActuatorMeshIntegration()
    await test_suite.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

