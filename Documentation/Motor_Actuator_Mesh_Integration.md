# Motor, Actuator, and Mesh Network Integration

## Overview
This document outlines the integration of motors, actuators, and the mesh network for the WDW Monorail System. The goal is to ensure compatibility and synchronization of all moving parts with the hybrid WiFi/Bluetooth mesh network.

## Components

### 1. Motors
Motors are responsible for propelling the monorails and controlling the movement of track switches and barn mechanisms.

#### Types of Motors
- **High-Torque Electric Motors:** Used for track switches to handle frequent switching operations.
- **Precision Electric Motors:** Used for monorails to ensure smooth acceleration and deceleration.
- **Precision Electric Motors (Barn):** Used for barn mechanisms to ensure accurate parking and alignment.

#### Motor Specifications
- **Motor ID:** Unique identifier for each motor.
- **Motor Type:** Type of motor (e.g., High-Torque Electric, Precision Electric).
- **Power Rating:** Power output in kW.
- **Torque:** Torque output in Nm.
- **Control Interface:** Interface for controlling the motor (e.g., PLC, Direct, Mesh).
- **Compatible Actuators:** List of actuators compatible with the motor.

### 2. Actuators
Actuators are responsible for controlling the movement of track switches, monorail components, and barn mechanisms.

#### Types of Actuators
- **Linear Actuators:** Used for track switches to move the concrete beam sections.
- **Rotary Actuators:** Used for monorail components to control the movement of monorail parts.
- **Linear Actuators (Barn):** Used for barn mechanisms to control the movement of monorail beams and slots.

#### Actuator Specifications
- **Actuator ID:** Unique identifier for each actuator.
- **Actuator Type:** Type of actuator (e.g., Linear Actuator, Rotary Actuator).
- **Stroke Length:** Length of stroke in mm.
- **Force:** Force output in N.
- **Control Interface:** Interface for controlling the actuator (e.g., PLC, Direct, Mesh).
- **Compatible Motors:** List of motors compatible with the actuator.

### 3. Mesh Network
The mesh network provides reliable and redundant communication between all moving parts and control systems.

#### Mesh Network Components
- **WiFi Mesh Network:** Provides high-bandwidth communication for data-intensive tasks.
- **Bluetooth Mesh Network:** Provides low-power, short-range communication for real-time data.
- **Mesh Nodes:** Individual nodes in the mesh network, representing monorails, switches, and other components.

#### Mesh Network Specifications
- **Mesh Node ID:** Unique identifier for each mesh node.
- **Bluetooth Address:** Bluetooth address for communication.
- **Position:** Current position of the mesh node.
- **Speed:** Current speed of the mesh node.
- **Status:** Current status of the mesh node (e.g., moving, stationary).
- **Peers:** List of other mesh nodes the current node is aware of.

## Integration

### Motor and Actuator Controller
The `MotorActuatorController` class is responsible for managing the motors and actuators, ensuring compatibility, and providing methods for checking compatibility and retrieving compatible components.

#### Methods
- **`add_motor(motor_spec: MotorSpec)`:** Add a motor to the controller.
- **`add_actuator(actuator_spec: ActuatorSpec)`:** Add an actuator to the controller.
- **`get_compatible_actuators(motor_id: str) -> List[str]`:** Get actuators compatible with a specific motor.
- **`get_compatible_motors(actuator_id: str) -> List[str]`:** Get motors compatible with a specific actuator.
- **`check_compatibility(motor_id: str, actuator_id: str) -> bool`:** Check if a motor and actuator are compatible.

### Mesh Network Integration
The `MeshNetworkMotorActuatorIntegration` class is responsible for integrating motors and actuators with the mesh network, ensuring that the status of motors and actuators is synchronized with the mesh network.

#### Methods
- **`add_mesh_node(mesh_node: MonorailMeshNode)`:** Add a mesh node to the integration.
- **`sync_motor_actuator_status(motor_id: str, actuator_id: str, mesh_node_id: str) -> bool`:** Sync the status of a motor and actuator with the mesh network.

### Switch Coordination
The `MonorailMeshNetwork` class is responsible for coordinating the passage of monorails through switch stations, ensuring that monorails can pass through switches safely and efficiently.

#### Methods
- **`add_monorail(monorail_id: str, bluetooth_address: str)`:** Add a monorail to the mesh network.
- **`add_switch(station_id: str, position: float, switch_type: str = "motor")`:** Add a switch station to the mesh network.
- **`handle_switch_passage(monorail_id: str, switch_id: str, incoming_route: str) -> bool`:** Coordinate monorail passage through a switch.
- **`check_collision_risk(monorail_id: str, next_position: float) -> bool`:** Check if a monorail moving to a specific position would collide with another monorail.

## Testing

### Test Script
The `test_motor_actuator_mesh_integration.py` script provides a comprehensive test suite for validating the integration of motors, actuators, and the mesh network. The test suite includes the following tests:

1. **Compatibility Test:** Validates the compatibility of motors and actuators.
2. **Mesh Integration Test:** Validates the integration of motors and actuators with the mesh network.
3. **Switch Coordination Test:** Validates the coordination of monorails through switch stations.
4. **Collision Detection Test:** Validates the collision detection mechanism.

### Running the Tests
To run the tests, execute the following command:

```bash
cd /home/workspace/WDW-Automated-Monorail-System/Scripts && python test_motor_actuator_mesh_integration.py
```

## Future Development

### Enhancements
1. **Advanced Motor Control:** Implement advanced motor control algorithms for smoother acceleration and deceleration.
2. **Predictive Maintenance:** Use sensor data to predict maintenance requirements and prevent failures.
3. **Energy Efficiency:** Optimize motor and actuator usage to reduce energy consumption.
4. **Enhanced Mesh Network:** Improve the mesh network's reliability and redundancy for better communication.

### Integration with Existing Systems
1. **PLC Integration:** Ensure seamless integration with existing PLC systems for controlling motors and actuators.
2. **Sensor Integration:** Integrate with existing sensor systems for monitoring motor and actuator performance.
3. **Control System Integration:** Ensure compatibility with existing control systems for managing the monorail system.

## Conclusion
The integration of motors, actuators, and the mesh network provides a robust and reliable system for controlling the WDW Monorail System. By ensuring compatibility and synchronization of all moving parts, the system can operate smoothly and efficiently, providing a better experience for passengers and staff alike.

