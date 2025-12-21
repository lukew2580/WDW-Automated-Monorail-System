#!/usr/bin/env python3
"""
WDW Monorail Raspberry Pi Dashboard

Dedicated Raspberry Pi interface for monorail control and monitoring.
Provides hardware integration, system status, and touch-friendly controls.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import platform
import psutil
import RPi.GPIO as GPIO
import board
import neopixel
import adafruit_character_lcd.character_lcd_rgb_backlight as character_lcd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)sZ %(levelname)s [RPi Dashboard] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger(__name__)

class RaspberryPiSystemMonitor:
    """Monitor Raspberry Pi system health and performance"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.last_update = datetime.now()
    
    def _get_system_info(self) -> Dict:
        """Get comprehensive Raspberry Pi system information"""
        try:
            # System information
            system_data = {
                'hostname': platform.node(),
                'os': platform.platform(),
                'python_version': platform.python_version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'uptime': str(timedelta(seconds=datetime.now().timestamp() - psutil.boot_time())),
                
                # CPU information
                'cpu_cores': psutil.cpu_count(logical=False),
                'cpu_logical_cores': psutil.cpu_count(logical=True),
                'cpu_usage': psutil.cpu_percent(interval=1),
                'cpu_frequency': psutil.cpu_freq()._asdict(),
                'cpu_temperature': self._get_cpu_temperature(),
                
                # Memory information
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'memory_used': psutil.virtual_memory().used,
                'memory_percent': psutil.virtual_memory().percent,
                
                # Disk information
                'disk_partitions': [p._asdict() for p in psutil.disk_partitions()],
                'disk_usage': psutil.disk_usage('/')._asdict(),
                
                # Network information
                'network_interfaces': self._get_network_info(),
                
                # Process information
                'process_count': len(psutil.pids()),
                'monorail_processes': self._get_monorail_processes(),
                
                'last_update': datetime.now().isoformat()
            }
            return system_data
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}
    
    def _get_cpu_temperature(self) -> Optional[float]:
        """Get Raspberry Pi CPU temperature"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000.0
                return round(temp, 1)
        except:
            return None
    
    def _get_network_info(self) -> List[Dict]:
        """Get network interface information"""
        interfaces = []
        for name, addrs in psutil.net_if_addrs().items():
            interface_info = {
                'name': name,
                'addresses': []
            }
            for addr in addrs:
                interface_info['addresses'].append({
                    'family': addr.family.name,
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                })
            interfaces.append(interface_info)
        return interfaces
    
    def _get_monorail_processes(self) -> List[Dict]:
        """Get information about running monorail processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                if proc.info['name'] and 'monorail' in proc.info['name'].lower():
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cmdline': proc.info['cmdline'],
                        'create_time': datetime.fromtimestamp(proc.info['create_time']).isoformat()
                    })
            except:
                continue
        return processes
    
    def update(self):
        """Update system information"""
        self.system_info = self._get_system_info()
        self.last_update = datetime.now()

class RaspberryPiHardwareController:
    """Control Raspberry Pi hardware components for monorail system"""
    
    def __init__(self):
        # GPIO setup
        self.gpio_mode = GPIO.BCM
        self.led_pins = {
            'status_red': 17,
            'status_green': 18,
            'status_blue': 27,
            'warning': 22,
            'emergency': 23
        }
        
        # NeoPixel setup
        self.pixel_pin = board.D18
        self.num_pixels = 30
        self.brightness = 0.2
        self.pixels = None
        
        # LCD setup
        self.lcd_columns = 16
        self.lcd_rows = 2
        self.lcd = None
        
        self._initialize_hardware()
    
    def _initialize_hardware(self):
        """Initialize all hardware components"""
        try:
            # Initialize GPIO
            GPIO.setmode(self.gpio_mode)
            GPIO.setwarnings(False)
            
            # Set up LED pins
            for pin in self.led_pins.values():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
            
            # Initialize NeoPixel strip
            self.pixels = neopixel.NeoPixel(
                self.pixel_pin, 
                self.num_pixels, 
                brightness=self.brightness, 
                auto_write=True
            )
            self.clear_leds()
            
            # Initialize LCD
            self._initialize_lcd()
            
            logger.info("Raspberry Pi hardware initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing hardware: {e}")
    
    def _initialize_lcd(self):
        """Initialize LCD display"""
        try:
            # LCD pin configuration
            lcd_rs = 25
            lcd_en = 24
            lcd_d4 = 23
            lcd_d5 = 17
            lcd_d6 = 18
            lcd_d7 = 22
            
            # Initialize LCD
            self.lcd = character_lcd.Character_LCD_RGB_Backlight(
                lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                self.lcd_columns, self.lcd_rows
            )
            self.lcd.clear()
            self.lcd.color = [100, 100, 100]  # White backlight
            
        except Exception as e:
            logger.warning(f"LCD initialization failed: {e}")
            self.lcd = None
    
    def set_status_led(self, color: str, state: bool):
        """Set status LED state"""
        if color in self.led_pins:
            GPIO.output(self.led_pins[color], GPIO.HIGH if state else GPIO.LOW)
    
    def clear_leds(self):
        """Turn off all LEDs"""
        for pin in self.led_pins.values():
            GPIO.output(pin, GPIO.LOW)
        if self.pixels:
            self.pixels.fill((0, 0, 0))
    
    def set_neopixel_color(self, color: Tuple[int, int, int]):
        """Set NeoPixel strip color"""
        if self.pixels:
            self.pixels.fill(color)
    
    def display_lcd_message(self, line1: str, line2: str = "", color: Tuple[int, int, int] = (100, 100, 100)):
        """Display message on LCD"""
        if self.lcd:
            self.lcd.clear()
            self.lcd.message = f"{line1[:16]}\n{line2[:16]}"
            self.lcd.color = color
    
    def cleanup(self):
        """Clean up hardware resources"""
        try:
            self.clear_leds()
            if self.lcd:
                self.lcd.clear()
            GPIO.cleanup()
            logger.info("Hardware cleanup completed")
        except Exception as e:
            logger.error(f"Error during hardware cleanup: {e}")

class RaspberryPiDashboard:
    """Main Raspberry Pi dashboard interface"""
    
    def __init__(self):
        self.system_monitor = RaspberryPiSystemMonitor()
        self.hardware_controller = RaspberryPiHardwareController()
        self.monorail_fleet = None
        self.line_tracker = None
        
        # Dashboard state
        self.current_view = "main"
        self.last_update = datetime.now()
        
        # Initialize dashboard
        self._initialize_dashboard()
    
    def _initialize_dashboard(self):
        """Initialize dashboard components"""
        logger.info("Initializing Raspberry Pi Dashboard")
        
        # Set initial hardware state
        self.hardware_controller.set_status_led('status_green', True)
        self.hardware_controller.display_lcd_message(
            "WDW Monorail", 
            "Initializing...",
            (0, 100, 0)  # Green
        )
        
        # Update system info
        self.system_monitor.update()
        
        logger.info("Dashboard initialized successfully")
    
    def update_system_status(self):
        """Update system status display"""
        try:
            # Update system monitor
            self.system_monitor.update()
            
            # Get current system info
            system_info = self.system_monitor.system_info
            
            # Update LCD display with system status
            cpu_temp = system_info.get('cpu_temperature', 'N/A')
            cpu_usage = system_info.get('cpu_usage', 'N/A')
            memory_usage = system_info.get('memory_percent', 'N/A')
            
            self.hardware_controller.display_lcd_message(
                f"CPU: {cpu_usage}% {cpu_temp}C",
                f"MEM: {memory_usage}%"
            )
            
            # Update status LEDs based on system health
            self._update_status_leds()
            
            self.last_update = datetime.now()
            logger.info("System status updated")
            
        except Exception as e:
            logger.error(f"Error updating system status: {e}")
    
    def _update_status_leds(self):
        """Update status LEDs based on system health"""
        try:
            system_info = self.system_monitor.system_info
            
            # Reset all status LEDs
            for color in ['status_red', 'status_green', 'status_blue']:
                self.hardware_controller.set_status_led(color, False)
            
            # Determine system health
            cpu_temp = system_info.get('cpu_temperature', 0)
            cpu_usage = system_info.get('cpu_usage', 0)
            memory_usage = system_info.get('memory_percent', 0)
            
            # Health indicators
            if cpu_temp > 70 or cpu_usage > 90 or memory_usage > 90:
                # Critical - Red
                self.hardware_controller.set_status_led('status_red', True)
                self.hardware_controller.set_status_led('warning', True)
            elif cpu_temp > 60 or cpu_usage > 80 or memory_usage > 80:
                # Warning - Yellow (Red + Green)
                self.hardware_controller.set_status_led('status_red', True)
                self.hardware_controller.set_status_led('status_green', True)
            else:
                # Normal - Green
                self.hardware_controller.set_status_led('status_green', True)
                
        except Exception as e:
            logger.error(f"Error updating status LEDs: {e}")
    
    def display_monorail_status(self, monorail_id: str, status: Dict):
        """Display monorail-specific status on dashboard"""
        try:
            # Extract key information
            line = status.get('line', 'N/A')
            position = status.get('position', 'N/A')
            speed = status.get('speed', 'N/A')
            health = status.get('health_status', 'N/A')
            
            # Update LCD
            self.hardware_controller.display_lcd_message(
                f"{monorail_id[:16]}",
                f"{line} {position}m"
            )
            
            # Update NeoPixel color based on health
            if health == 'critical':
                self.hardware_controller.set_neopixel_color((255, 0, 0))  # Red
            elif health == 'warning':
                self.hardware_controller.set_neopixel_color((255, 165, 0))  # Orange
            elif health == 'normal':
                self.hardware_controller.set_neopixel_color((0, 255, 0))  # Green
            else:
                self.hardware_controller.set_neopixel_color((0, 0, 255))  # Blue
                
            logger.info(f"Displaying status for {monorail_id}: {status}")
            
        except Exception as e:
            logger.error(f"Error displaying monorail status: {e}")
    
    def show_alert(self, message: str, alert_type: str = 'info'):
        """Show alert on dashboard"""
        try:
            # Set LCD display
            if alert_type == 'critical':
                self.hardware_controller.display_lcd_message(
                    "CRITICAL ALERT",
                    message[:16],
                    (255, 0, 0)  # Red
                )
                self.hardware_controller.set_status_led('emergency', True)
                self.hardware_controller.set_neopixel_color((255, 0, 0))
                
            elif alert_type == 'warning':
                self.hardware_controller.display_lcd_message(
                    "WARNING",
                    message[:16],
                    (255, 165, 0)  # Orange
                )
                self.hardware_controller.set_status_led('warning', True)
                self.hardware_controller.set_neopixel_color((255, 165, 0))
                
            else:  # info
                self.hardware_controller.display_lcd_message(
                    "INFO",
                    message[:16],
                    (0, 100, 255)  # Blue
                )
                self.hardware_controller.set_neopixel_color((0, 100, 255))
            
            logger.info(f"Alert displayed: {alert_type} - {message}")
            
        except Exception as e:
            logger.error(f"Error showing alert: {e}")
    
    def clear_alert(self):
        """Clear current alert"""
        try:
            self.hardware_controller.set_status_led('emergency', False)
            self.hardware_controller.set_status_led('warning', False)
            self.update_system_status()
            logger.info("Alert cleared")
            
        except Exception as e:
            logger.error(f"Error clearing alert: {e}")
    
    def get_system_info(self) -> Dict:
        """Get current system information"""
        return self.system_monitor.system_info
    
    def get_hardware_status(self) -> Dict:
        """Get hardware controller status"""
        return {
            'led_status': {color: GPIO.input(pin) for color, pin in self.hardware_controller.led_pins.items()},
            'lcd_connected': self.hardware_controller.lcd is not None,
            'neopixel_connected': self.hardware_controller.pixels is not None,
            'last_update': self.last_update.isoformat()
        }
    
    def cleanup(self):
        """Clean up dashboard resources"""
        try:
            self.hardware_controller.cleanup()
            logger.info("Dashboard cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during dashboard cleanup: {e}")

async def main():
    """Main dashboard application"""
    logger.info("Starting WDW Monorail Raspberry Pi Dashboard")
    
    try:
        # Create dashboard instance
        dashboard = RaspberryPiDashboard()
        
        # Main dashboard loop
        while True:
            # Update system status
            dashboard.update_system_status()
            
            # Simulate monorail status updates (in real system, this would come from actual data)
            # For demo purposes, we'll cycle through different monorails
            import time
            monorails = ["Red", "Blue", "Green", "Yellow"]
            for i, monorail in enumerate(monorails):
                dashboard.display_monorail_status(monorail, {
                    'line': 'Resort' if i % 2 == 0 else 'Express',
                    'position': 1000 + i * 500,
                    'speed': 25 + i * 5,
                    'health_status': 'normal'
                })
                await asyncio.sleep(3)
            
            # Show different alert types for demonstration
            dashboard.show_alert("System check complete", "info")
            await asyncio.sleep(2)
            
            dashboard.show_alert("High CPU usage detected", "warning")
            await asyncio.sleep(2)
            
            dashboard.clear_alert()
            
            # Update every 30 seconds
            await asyncio.sleep(30)
            
    except KeyboardInterrupt:
        logger.info("Dashboard shutting down...")
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
    finally:
        # Clean up resources
        if 'dashboard' in locals():
            dashboard.cleanup()
        logger.info("Dashboard stopped")

if __name__ == "__main__":
    asyncio.run(main())
