#!/usr/bin/env python3
"""
Bluetooth Hardware Pairing
Real Bluetooth LE communication with monorail hardware
"""

import logging
import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO, format="%(asctime)sZ %(levelname)s %(message)s")

try:
    from bleak import BleakClient, BleakScanner
    BLEAK_AVAILABLE = True
except ImportError:
    BLEAK_AVAILABLE = False
    logging.warning("bleak not available - using mock Bluetooth")

@dataclass
class BluetoothDevice:
    """Bluetooth device configuration"""
    address: str
    name: str
    train_id: str
    uuid_control: str
    uuid_telemetry: str
    uuid_status: str

class MonorailBluetoothController:
    """Real Bluetooth LE communication with monorail trains"""
    
    # Standard Bluetooth UUIDs for custom services
    MONORAIL_SERVICE_UUID = "12345678-1234-1234-1234-123456789012"
    CONTROL_CHAR_UUID = "11111111-1111-1111-1111-111111111111"
    TELEMETRY_CHAR_UUID = "22222222-2222-2222-2222-222222222222"
    STATUS_CHAR_UUID = "33333333-3333-3333-3333-333333333333"
    
    def __init__(self):
        self.devices: Dict[str, BluetoothDevice] = {}
        self.clients: Dict[str, Optional[BleakClient]] = {}
        self.connected_trains = set()
        self.telemetry_callbacks: Dict[str, List[Callable]] = {}
        self.setup_monorails()
    
    def setup_monorails(self):
        """Configure known monorail Bluetooth devices"""
        monorails = [
            BluetoothDevice(
                address="AA:BB:CC:DD:EE:01",
                name="Monorail-Red",
                train_id="monorail_red",
                uuid_control=self.CONTROL_CHAR_UUID,
                uuid_telemetry=self.TELEMETRY_CHAR_UUID,
                uuid_status=self.STATUS_CHAR_UUID
            ),
            BluetoothDevice(
                address="AA:BB:CC:DD:EE:02",
                name="Monorail-Orange",
                train_id="monorail_orange",
                uuid_control=self.CONTROL_CHAR_UUID,
                uuid_telemetry=self.TELEMETRY_CHAR_UUID,
                uuid_status=self.STATUS_CHAR_UUID
            ),
            BluetoothDevice(
                address="AA:BB:CC:DD:EE:03",
                name="Monorail-Yellow",
                train_id="monorail_yellow",
                uuid_control=self.CONTROL_CHAR_UUID,
                uuid_telemetry=self.TELEMETRY_CHAR_UUID,
                uuid_status=self.STATUS_CHAR_UUID
            ),
            BluetoothDevice(
                address="AA:BB:CC:DD:EE:04",
                name="Monorail-Green",
                train_id="monorail_green",
                uuid_control=self.CONTROL_CHAR_UUID,
                uuid_telemetry=self.TELEMETRY_CHAR_UUID,
                uuid_status=self.STATUS_CHAR_UUID
            ),
        ]
        
        for device in monorails:
            self.devices[device.train_id] = device
            self.clients[device.train_id] = None
            self.telemetry_callbacks[device.train_id] = []
        
        logging.info(f"Configured {len(monorails)} Bluetooth monorails")
    
    async def discover_devices(self) -> List[str]:
        """Scan for Bluetooth LE devices"""
        if not BLEAK_AVAILABLE:
            logging.info("🔍 Using mock device discovery")
            return list(self.devices.keys())
        
        try:
            logging.info("🔍 Scanning for Bluetooth devices...")
            devices = await BleakScanner.discover()
            found = []
            
            for device in devices:
                for train_id, config in self.devices.items():
                    if config.address.lower() == device.address.lower():
                        found.append(train_id)
                        logging.info(f"  ✓ Found {config.name}")
            
            return found
        except Exception as e:
            logging.error(f"Discovery failed: {e}")
            return []
    
    async def connect(self, train_id: str) -> bool:
        """Connect to a monorail via Bluetooth"""
        if train_id not in self.devices:
            logging.error(f"Unknown train: {train_id}")
            return False
        
        device = self.devices[train_id]
        
        if not BLEAK_AVAILABLE:
            logging.info(f"✓ Mock connected to {device.name}")
            self.connected_trains.add(train_id)
            return True
        
        try:
            logging.info(f"Connecting to {device.name} ({device.address})...")
            client = BleakClient(device.address)
            await client.connect()
            self.clients[train_id] = client
            self.connected_trains.add(train_id)
            logging.info(f"✓ Connected to {device.name}")
            return True
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            return False
    
    async def disconnect(self, train_id: str) -> bool:
        """Disconnect from a monorail"""
        if train_id not in self.devices:
            return False
        
        if not BLEAK_AVAILABLE or self.clients[train_id] is None:
            self.connected_trains.discard(train_id)
            logging.info(f"Mock disconnected from {self.devices[train_id].name}")
            return True
        
        try:
            await self.clients[train_id].disconnect()
            self.connected_trains.discard(train_id)
            logging.info(f"✓ Disconnected from {self.devices[train_id].name}")
            return True
        except Exception as e:
            logging.error(f"Disconnection failed: {e}")
            return False
    
    async def send_command(self, train_id: str, command: Dict) -> bool:
        """Send control command to monorail"""
        if train_id not in self.connected_trains:
            logging.warning(f"{train_id} not connected")
            return False
        
        device = self.devices[train_id]
        command_str = f"{command['action']}:{command.get('speed', 0)}:{command.get('direction', 'stop')}"
        
        if not BLEAK_AVAILABLE:
            logging.info(f"→ {device.name}: {command_str}")
            return True
        
        try:
            client = self.clients[train_id]
            if client and client.is_connected:
                await client.write_gatt_char(
                    device.uuid_control,
                    command_str.encode()
                )
                logging.info(f"→ {device.name}: {command_str}")
                return True
        except Exception as e:
            logging.error(f"Command failed: {e}")
            return False
    
    async def read_telemetry(self, train_id: str) -> Optional[Dict]:
        """Read telemetry data from monorail"""
        if train_id not in self.connected_trains:
            return None
        
        device = self.devices[train_id]
        
        if not BLEAK_AVAILABLE:
            return {
                "speed": 45.5,
                "position": 2500,
                "voltage": 12.0,
                "temperature": 65,
                "signal_strength": -55
            }
        
        try:
            client = self.clients[train_id]
            if client and client.is_connected:
                data = await client.read_gatt_char(device.uuid_telemetry)
                # Parse telemetry data
                return {
                    "raw": data.decode(),
                    "timestamp": asyncio.get_event_loop().time()
                }
        except Exception as e:
            logging.error(f"Telemetry read failed: {e}")
            return None
    
    async def register_telemetry_callback(self, train_id: str, callback: Callable):
        """Register callback for telemetry updates"""
        if train_id in self.telemetry_callbacks:
            self.telemetry_callbacks[train_id].append(callback)
    
    def get_connection_status(self) -> Dict:
        """Get connection status for all trains"""
        return {
            train_id: {
                "name": self.devices[train_id].name,
                "connected": train_id in self.connected_trains,
                "address": self.devices[train_id].address
            }
            for train_id in self.devices.keys()
        }

async def demo_bluetooth():
    """Demo Bluetooth pairing and communication"""
    logging.info("=" * 70)
    logging.info("WDW Monorail - Bluetooth Hardware Pairing")
    logging.info("=" * 70)
    
    controller = MonorailBluetoothController()
    
    # Discover devices
    logging.info("\n🔍 Discovering devices...")
    found = await controller.discover_devices()
    logging.info(f"Found {len(found)} monorails")
    
    # Connect to monorails
    logging.info("\n📱 Connecting to monorails...")
    for train_id in ["monorail_red", "monorail_orange", "monorail_yellow"]:
        await controller.connect(train_id)
        await asyncio.sleep(0.5)
    
    # Send commands
    logging.info("\n📤 Sending control commands...")
    await controller.send_command("monorail_red", {"action": "start", "speed": 75, "direction": "forward"})
    await controller.send_command("monorail_orange", {"action": "start", "speed": 60, "direction": "forward"})
    
    # Read telemetry
    logging.info("\n📡 Reading telemetry...")
    for train_id in ["monorail_red", "monorail_orange"]:
        telemetry = await controller.read_telemetry(train_id)
        if telemetry:
            logging.info(f"  {train_id}: {telemetry}")
    
    # Status report
    logging.info("\n📊 Connection Status:")
    status = controller.get_connection_status()
    for train_id, info in status.items():
        conn = "✓" if info["connected"] else "✗"
        logging.info(f"  {conn} {info['name']}: {info['address']}")
    
    # Disconnect
    logging.info("\n🔌 Disconnecting...")
    for train_id in controller.connected_trains.copy():
        await controller.disconnect(train_id)
    
    logging.info("\n" + "=" * 70)
    logging.info("✅ Bluetooth pairing demo complete!")
    logging.info("=" * 70)

if __name__ == "__main__":
    asyncio.run(demo_bluetooth())

