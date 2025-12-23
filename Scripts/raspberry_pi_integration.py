#!/usr/bin/env python3
"""
Raspberry Pi GPIO Integration
Controls monorail motors, switches, and sensors via GPIO
"""

import logging
import asyncio
from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

# Mock GPIO for testing (real implementation uses RPi.GPIO or gpiozero)
class MockGPIO:
    def __init__(self):
        self.pins = {}
    
    def setup(self, pin, mode):
        self.pins[pin] = {"mode": mode, "state": 0}
    
    def output(self, pin, state):
        if pin in self.pins:
            self.pins[pin]["state"] = state
    
    def input(self, pin):
        return self.pins.get(pin, {}).get("state", 0)
    
    def cleanup(self):
        self.pins.clear()

class MotorDirection(Enum):
    FORWARD = 1
    REVERSE = -1
    STOP = 0

@dataclass
class GPIOPin:
    """GPIO Pin configuration"""
    pin_number: int
    name: str
    mode: str  # "IN" or "OUT"
    function: str  # motor, sensor, switch, etc.

class RaspberryPiController:
    """Manage monorail hardware via Raspberry Pi GPIO"""
    
    def __init__(self, enable_hardware=False):
        self.enable_hardware = enable_hardware
        self.gpio = MockGPIO()
        self.motors = {}
        self.sensors = {}
        self.switches = {}
        self.setup_pins()
    
    def setup_pins(self):
        """Configure GPIO pins for monorail system"""
        # Motor control pins (using L298N motor driver)
        motor_pins = {
            "monorail_red": {"in1": 17, "in2": 27, "en": 22, "pwm_freq": 1000},
            "monorail_orange": {"in1": 23, "in2": 24, "en": 25, "pwm_freq": 1000},
            "monorail_yellow": {"in1": 5, "in2": 6, "en": 13, "pwm_freq": 1000},
            "monorail_green": {"in1": 12, "in2": 16, "en": 26, "pwm_freq": 1000},
        }
        
        for train, pins in motor_pins.items():
            self.motors[train] = {
                "in1": pins["in1"],
                "in2": pins["in2"],
                "enable": pins["en"],
                "speed": 0,
                "direction": MotorDirection.STOP,
                "pwm": None
            }
            self.gpio.setup(pins["in1"], "OUT")
            self.gpio.setup(pins["in2"], "OUT")
            self.gpio.setup(pins["en"], "OUT")
        
        # Sensor pins (proximity, position, speed)
        sensor_pins = {
            "ttr_sensor": 4,
            "mk_sensor": 14,
            "epcot_sensor": 15,
            "hs_sensor": 18,
            "ak_sensor": 19,
        }
        
        for sensor, pin in sensor_pins.items():
            self.sensors[sensor] = {"pin": pin, "value": 0}
            self.gpio.setup(pin, "IN")
        
        # Switch control pins (track switches, turnouts)
        switch_pins = {
            "ttr_mk_switch": 20,
            "mk_bypass_switch": 21,
            "epcot_switch": 10,
            "resort_switch": 11,
        }
        
        for switch, pin in switch_pins.items():
            self.switches[switch] = {"pin": pin, "position": 0}
            self.gpio.setup(pin, "OUT")
        
        logging.info("GPIO pins configured for 4 monorails + sensors + switches")
    
    async def set_motor_speed(self, train_id: str, speed: float, direction: MotorDirection):
        """
        Set motor speed and direction
        speed: 0-100 (percentage)
        direction: FORWARD, REVERSE, STOP
        """
        if train_id not in self.motors:
            logging.error(f"Unknown train: {train_id}")
            return False
        
        motor = self.motors[train_id]
        motor["speed"] = max(0, min(100, speed))
        motor["direction"] = direction
        
        # Control motor direction
        if direction == MotorDirection.FORWARD:
            self.gpio.output(motor["in1"], 1)
            self.gpio.output(motor["in2"], 0)
        elif direction == MotorDirection.REVERSE:
            self.gpio.output(motor["in1"], 0)
            self.gpio.output(motor["in2"], 1)
        else:  # STOP
            self.gpio.output(motor["in1"], 0)
            self.gpio.output(motor["in2"], 0)
        
        # Set speed via PWM (0-100)
        self.gpio.output(motor["enable"], int(motor["speed"]))
        
        logging.info(f"{train_id}: {direction.name} @ {motor['speed']}%")
        return True
    
    async def read_sensor(self, sensor_id: str) -> int:
        """Read sensor value"""
        if sensor_id not in self.sensors:
            return 0
        
        sensor = self.sensors[sensor_id]
        value = self.gpio.input(sensor["pin"])
        sensor["value"] = value
        return value
    
    async def set_switch_position(self, switch_id: str, position: int):
        """Control track switch (0 or 1)"""
        if switch_id not in self.switches:
            logging.error(f"Unknown switch: {switch_id}")
            return False
        
        switch = self.switches[switch_id]
        switch["position"] = max(0, min(1, position))
        self.gpio.output(switch["pin"], switch["position"])
        
        logging.info(f"{switch_id}: Position {switch['position']}")
        return True
    
    async def emergency_stop(self):
        """Emergency stop all motors"""
        for train_id in self.motors.keys():
            await self.set_motor_speed(train_id, 0, MotorDirection.STOP)
        logging.warning("EMERGENCY STOP - All motors halted")
    
    def get_system_status(self) -> Dict:
        """Get current hardware status"""
        return {
            "motors": {
                name: {
                    "speed": motor["speed"],
                    "direction": motor["direction"].name,
                }
                for name, motor in self.motors.items()
            },
            "sensors": {
                name: sensor["value"]
                for name, sensor in self.sensors.items()
            },
            "switches": {
                name: switch["position"]
                for name, switch in self.switches.items()
            }
        }

async def demo_rpi_control():
    """Demo Raspberry Pi GPIO control"""
    logging.info("=" * 70)
    logging.info("WDW Monorail - Raspberry Pi GPIO Integration")
    logging.info("=" * 70)
    
    controller = RaspberryPiController(enable_hardware=False)
    
    # Demo: Run Monorail Red forward
    logging.info("\n🚂 Starting Monorail Red...")
    await controller.set_motor_speed("monorail_red", 75, MotorDirection.FORWARD)
    await asyncio.sleep(2)
    
    # Demo: Check sensors
    logging.info("\n📡 Reading track sensors...")
    for sensor in ["ttr_sensor", "mk_sensor", "epcot_sensor"]:
        value = await controller.read_sensor(sensor)
        logging.info(f"  {sensor}: {value}")
    
    # Demo: Control switches
    logging.info("\n🔄 Setting track switches...")
    await controller.set_switch_position("ttr_mk_switch", 1)
    await controller.set_switch_position("resort_switch", 0)
    
    # Demo: Emergency stop
    logging.info("\n🛑 Testing emergency stop...")
    await controller.emergency_stop()
    
    # Status report
    logging.info("\n📊 System Status:")
    status = controller.get_system_status()
    logging.info(f"Motors: {status['motors']}")
    logging.info(f"Sensors: {status['sensors']}")
    logging.info(f"Switches: {status['switches']}")
    
    logging.info("\n" + "=" * 70)
    logging.info("✅ Raspberry Pi integration demo complete!")
    logging.info("=" * 70)

if __name__ == "__main__":
    asyncio.run(demo_rpi_control())

