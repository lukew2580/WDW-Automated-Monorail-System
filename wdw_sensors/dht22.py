import Adafruit_DHT

class DHT22:
    """
    DHT22 Temperature and Humidity Sensor
    
    Args:
        pin (int): GPIO pin number
        fast_mode (bool): Enable fast mode for 1Hz updates
    """
    def __init__(self, pin=4, fast_mode=False):
        self.sensor = Adafruit_DHT.DHT22
        self.pin = pin
        self.fast_mode = fast_mode
    
    def read(self):
        """Read temperature and humidity data"""
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return {"temperature": temperature, "humidity": humidity}
    
    def read_fast(self):
        """Read temperature and humidity data in fast mode"""
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin, retry_limit=1)
        return {"temperature": temperature, "humidity": humidity}
