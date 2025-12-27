import smbus
import time

class MPU6050:
    """
    MPU6050 Accelerometer and Gyroscope Sensor
    
    Args:
        address (int): I2C address (default: 0x68)
        bus (int): I2C bus number (default: 1)
    """
    def __init__(self, address=0x68, bus=1):
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.initialize()
    
    def initialize(self):
        """Initialize the MPU6050 sensor"""
        # Power management register
        self.bus.write_byte_data(self.address, 0x6B, 0)
        time.sleep(0.1)
    
    def read(self):
        """Read accelerometer and gyroscope data"""
        # Read accelerometer data
        accel_x = self._read_word(0x3B)
        accel_y = self._read_word(0x3D)
        accel_z = self._read_word(0x3F)
        
        # Read gyroscope data
        gyro_x = self._read_word(0x43)
        gyro_y = self._read_word(0x45)
        gyro_z = self._read_word(0x47)
        
        return {
            "accel": {"x": accel_x, "y": accel_y, "z": accel_z},
            "gyro": {"x": gyro_x, "y": gyro_y, "z": gyro_z}
        }
    
    def _read_word(self, addr):
        """Read a 16-bit value from the MPU6050"""
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) + low
        return value if value < 32768 else value - 65536
