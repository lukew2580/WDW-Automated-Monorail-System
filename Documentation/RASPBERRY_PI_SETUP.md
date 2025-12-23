# WDW Monorail System - Raspberry Pi Setup Guide

## 🍓 Raspberry Pi Installation & Configuration

This guide provides comprehensive instructions for setting up the WDW Monorail System on Raspberry Pi hardware.

## 📋 System Requirements

### **Hardware Requirements**

| Component | Specification | Quantity |
|-----------|---------------|----------|
| Raspberry Pi | Pi 4 Model B (4GB+) recommended | 1 |
| Power Supply | 5V 3A USB-C | 1 |
| MicroSD Card | 32GB+ Class 10 UHS-I | 1 |
| Cooling | Heat sinks + fan (recommended) | 1 |
| Case | Protective case with access | 1 |
| GPIO Components | LEDs, buttons, sensors | Various |
| LCD Display | 16x2 Character LCD with RGB backlight | 1 |
| NeoPixel Strip | WS2812B LED strip (30 LEDs) | 1 |
| Network | WiFi or Ethernet connection | 1 |

### **Software Requirements**

- **Raspberry Pi OS**: Raspberry Pi OS Lite (64-bit) recommended
- **Python**: Python 3.9+
- **Dependencies**: See `requirements.txt`
- **Additional Packages**: GPIO libraries, I2C tools

## 🛠️ Raspberry Pi OS Setup

### **1. Install Raspberry Pi OS**

```bash
# Download Raspberry Pi Imager
# https://www.raspberrypi.com/software/

# Select:
# - Raspberry Pi OS (other) > Raspberry Pi OS Lite (64-bit)
# - Your SD card
# - Write
```

### **2. Enable SSH and WiFi (Headless Setup)**

Before inserting the SD card:

1. Create empty file named `ssh` in boot partition
2. Create `wpa_supplicant.conf` in boot partition:

```conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YourWiFiName"
    psk="YourWiFiPassword"
    key_mgmt=WPA-PSK
}
```

### **3. Boot and Initial Configuration**

```bash
# SSH into your Pi (default password: raspberry)
ssh pi@raspberrypi.local

# Run raspi-config
sudo raspi-config
```

**Recommended settings:**
- System Options > Hostname: `wdw-monorail-control`
- System Options > Boot / Auto Login: `Console Autologin`
- Interface Options > I2C: Enable
- Interface Options > SPI: Enable
- Interface Options > Serial: Disable shell, Enable hardware
- Performance Options > GPU Memory: 16MB
- Localisation Options: Set timezone, keyboard layout

### **4. Update System**

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git i2c-tools libatlas-base-dev
```

## 🐍 Python Environment Setup

### **1. Create Virtual Environment**

```bash
python3 -m venv ~/wdw-monorail-venv
source ~/wdw-monorail-venv/bin/activate
```

### **2. Install Dependencies**

```bash
# Install system dependencies
sudo apt install -y python3-rpi.gpio python3-smbus python3-pil

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install Raspberry Pi specific packages
pip install adafruit-circuitpython-rgb-display adafruit-circuitpython-neopixel
```

### **3. Enable I2C and SPI**

```bash
# Add to /boot/config.txt
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Reboot
sudo reboot
```

## 🔌 Hardware Setup

### **1. GPIO Pinout Reference**

```
WDW Monorail System GPIO Configuration:

Status LEDs:
  - Red:     GPIO 17 (Pin 11)
  - Green:   GPIO 18 (Pin 12)
  - Blue:    GPIO 27 (Pin 13)
  - Warning: GPIO 22 (Pin 15)
  - Emergency: GPIO 23 (Pin 16)

LCD Display (I2C):
  - SDA:     GPIO 2 (Pin 3)
  - SCL:     GPIO 3 (Pin 5)

NeoPixel Strip:
  - Data:    GPIO 18 (Pin 12)
  - Power:   5V (Pin 2 or 4)
  - Ground:  GND (Pin 6, 9, 14, etc.)

Monorail Control (L298N Motor Drivers):
  - Red:     GPIO 17, 27, 22
  - Orange:  GPIO 23, 24, 25
  - Yellow:  GPIO 5, 6, 13
  - Green:   GPIO 12, 16, 26
```

### **2. LCD Display Setup**

1. Connect LCD via I2C backpack:
   - SDA → GPIO 2 (Pin 3)
   - SCL → GPIO 3 (Pin 5)
   - 5V → 5V (Pin 2 or 4)
   - GND → GND (Pin 6)

2. Test I2C connection:
   ```bash
   sudo i2cdetect -y 1
   ```
   Should show device at 0x27 or similar.

### **3. NeoPixel Strip Setup**

1. Connect NeoPixel strip:
   - Data → GPIO 18 (Pin 12)
   - 5V → 5V power supply (external recommended)
   - GND → GND

2. Add power protection:
   - 1000µF capacitor across power lines
   - 300-500Ω resistor on data line

### **4. Status LEDs Setup**

Connect LEDs with appropriate resistors (220Ω recommended):
- Anode (long leg) → GPIO pin
- Cathode (short leg) → GND through resistor

## 🚂 Monorail System Installation

### **1. Clone Repository**

```bash
cd ~
git clone https://github.com/lukew2580/WDW-Automated-Monorail-System.git
cd WDW-Automated-Monorail-System
```

### **2. Configure System**

```bash
# Copy configuration template
cp config_template.json config.json

# Edit configuration
nano config.json
```

### **3. Test Hardware**

```bash
# Test GPIO
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('GPIO OK')"

# Test I2C
python3 -c "import smbus2; print('I2C OK')"

# Test NeoPixel
python3 -c "import neopixel; print('NeoPixel OK')"
```

## 📊 Dashboard Configuration

### **1. Raspberry Pi Dashboard Setup**

Edit `raspberry_pi_dashboard.py` to configure:
- GPIO pin assignments
- LCD parameters
- NeoPixel configuration
- System monitoring intervals

### **2. Hardware Calibration**

```python
# In raspberry_pi_dashboard.py, adjust these parameters:

# LED brightness levels
LED_BRIGHTNESS = {
    'low': 0.1,
    'medium': 0.5,
    'high': 1.0
}

# LCD contrast (0-255)
LCD_CONTRAST = 60

# NeoPixel brightness (0.0-1.0)
NEOPIXEL_BRIGHTNESS = 0.2

# System monitoring intervals
SYSTEM_UPDATE_INTERVAL = 30  # seconds
MONORAIL_UPDATE_INTERVAL = 5  # seconds
```

## 🎛️ Dashboard Features

### **Main Dashboard Views**

1. **System Status View**
   - CPU usage and temperature
   - Memory utilization
   - Disk space
   - Network status
   - Process monitoring

2. **Monorail Fleet View**
   - Real-time position tracking
   - Speed and direction
   - Health status indicators
   - Line assignments

3. **Alert System**
   - Critical alerts (red)
   - Warning alerts (orange)
   - Informational alerts (blue)
   - Visual and audible indicators

4. **Hardware Control**
   - Manual override controls
   - Emergency stop
   - System reset
   - Maintenance mode

### **Visual Indicators**

| Indicator | Color | Meaning |
|-----------|-------|---------|
| Status LED | Green | System normal |
| Status LED | Yellow | Warning condition |
| Status LED | Red | Critical alert |
| Warning LED | Yellow | Attention required |
| Emergency LED | Red | Emergency situation |
| NeoPixel | Green | Normal operation |
| NeoPixel | Orange | Warning state |
| NeoPixel | Red | Critical state |
| NeoPixel | Blue | Information/standby |

## 🔄 System Management

### **1. Starting the Dashboard**

```bash
# Activate virtual environment
source ~/wdw-monorail-venv/bin/activate

# Start dashboard
cd ~/WDW-Automated-Monorail-System
python3 raspberry_pi_dashboard.py
```

### **2. Running as Service**

```bash
# Create systemd service
sudo nano /etc/systemd/system/wdw-monorail-dashboard.service
```

```ini
[Unit]
Description=WDW Monorail Raspberry Pi Dashboard
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/WDW-Automated-Monorail-System
Environment="PATH=/home/pi/wdw-monorail-venv/bin"
ExecStart=/home/pi/wdw-monorail-venv/bin/python3 raspberry_pi_dashboard.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable wdw-monorail-dashboard
sudo systemctl start wdw-monorail-dashboard

# Check status
sudo systemctl status wdw-monorail-dashboard

# View logs
journalctl -u wdw-monorail-dashboard -f
```

### **3. Updating the System**

```bash
# Pull latest changes
cd ~/WDW-Automated-Monorail-System
git pull origin main

# Update dependencies
source ~/wdw-monorail-venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl restart wdw-monorail-dashboard
```

## 🛡️ Security Configuration

### **1. Secure SSH Access**

```bash
# Change default password
passwd

# Disable password authentication (use SSH keys)
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart ssh

# Set up firewall
sudo apt install ufw
sudo ufw allow 22
sudo ufw enable
```

### **2. System Hardening**

```bash
# Update regularly
sudo apt update && sudo apt upgrade -y

# Install fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban

# Secure shared memory
sudo nano /etc/fstab
# Add: tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0
sudo reboot
```

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### **I2C Not Detected**
```bash
# Check if I2C is enabled
lsmod | grep i2c

# Enable I2C
sudo raspi-config nonint do_i2c 0
sudo reboot

# Check I2C devices
sudo i2cdetect -y 1
```

#### **GPIO Permission Errors**
```bash
# Add user to GPIO group
sudo usermod -aG gpio pi

# Check permissions
ls -l /dev/gpiomem

# Reboot
sudo reboot
```

#### **NeoPixel Issues**
```bash
# Check power supply (NeoPixels need adequate power)
# Verify data line resistor (300-500Ω recommended)
# Test with simple script:
python3 -c "
import neopixel
import board
pixels = neopixel.NeoPixel(board.D18, 30, brightness=0.1)
pixels.fill((255, 0, 0))
"
```

#### **Dashboard Not Starting**
```bash
# Check logs
journalctl -u wdw-monorail-dashboard -f

# Test manually
source ~/wdw-monorail-venv/bin/activate
python3 raspberry_pi_dashboard.py

# Check dependencies
pip list
```

## 📈 Performance Optimization

### **1. Raspberry Pi Optimization**

```bash
# Overclocking (use with caution)
sudo raspi-config
# Performance Options > Overclock

# Memory split
sudo raspi-config
# Performance Options > GPU Memory: 16MB

# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable hciuart
```

### **2. Python Performance**

```bash
# Install performance packages
pip install numba numpy

# Use PyPy for performance-critical sections
sudo apt install pypy3
```

### **3. System Monitoring**

```bash
# Install monitoring tools
sudo apt install htop iotop iftop

# Monitor system
htop

# Monitor I/O
iotop

# Monitor network
iftop
```

## 🎯 Advanced Configuration

### **1. Custom GPIO Mapping**

Edit `raspberry_pi_dashboard.py` to customize GPIO assignments:

```python
# Customize LED pins
led_pins = {
    'status_red': 17,
    'status_green': 18,
    'status_blue': 27,
    'warning': 22,
    'emergency': 23
}

# Customize NeoPixel configuration
pixel_pin = board.D18
num_pixels = 30
brightness = 0.2
```

### **2. LCD Customization**

```python
# Customize LCD parameters
lcd_columns = 16
lcd_rows = 2
lcd_i2c_address = 0x27  # Check with i2cdetect
lcd_contrast = 60
```

### **3. Alert System Customization**

```python
# Customize alert thresholds
ALERT_THRESHOLDS = {
    'cpu_temperature_critical': 75.0,  # °C
    'cpu_temperature_warning': 70.0,  # °C
    'cpu_usage_critical': 95.0,      # %
    'cpu_usage_warning': 90.0,       # %
    'memory_usage_critical': 95.0,   # %
    'memory_usage_warning': 90.0,    # %
    'disk_usage_critical': 95.0,     # %
    'disk_usage_warning': 90.0       # %
}
```

## 🌐 Network Configuration

### **1. Static IP Setup**

```bash
sudo nano /etc/dhcpcd.conf
```

```conf
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8

interface wlan0
static ip_address=192.168.1.101/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

### **2. WiFi Configuration**

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

```conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="WDW-Monorail-Network"
    psk="securepassword"
    key_mgmt=WPA-PSK
    priority=10
}

network={
    ssid="Backup-Network"
    psk="backupassword"
    key_mgmt=WPA-PSK
    priority=5
}
```

## 🔄 Backup & Recovery

### **1. System Backup**

```bash
# Backup SD card (from another computer)
sudo dd if=/dev/sdX of=wdw-monorail-backup.img bs=4M status=progress

# Compress backup
sudo pigz wdw-monorail-backup.img

# Restore backup
sudo pigz -d wdw-monorail-backup.img.gz
sudo dd if=wdw-monorail-backup.img of=/dev/sdX bs=4M status=progress
```

### **2. Configuration Backup**

```bash
# Backup configuration
cd ~/WDW-Automated-Monorail-System
tar czvf config_backup.tar.gz config.json raspberry_pi_dashboard.py

# Restore configuration
tar xzvf config_backup.tar.gz
```

## 📚 Additional Resources

### **Raspberry Pi Documentation**
- [Raspberry Pi Official Documentation](https://www.raspberrypi.com/documentation/)
- [RPi GPIO Usage](https://www.raspberrypi.com/documentation/computers/os.html#gpio)
- [I2C Configuration](https://www.raspberrypi.com/documentation/computers/configuration.html#i2c)

### **Hardware Resources**
- [Adafruit NeoPixel Guide](https://learn.adafruit.com/adafruit-neopixel-uberguide)
- [LCD Character Display Guide](https://learn.adafruit.com/character-lcds)
- [RPi GPIO Pinout](https://pinout.xyz/)

### **Software Resources**
- [CircuitPython Libraries](https://circuitpython.org/libraries)
- [RPi.GPIO Documentation](https://pypi.org/project/RPi.GPIO/)
- [Python Asyncio Guide](https://docs.python.org/3/library/asyncio.html)

## 🎓 Best Practices

### **1. Power Management**
- Use high-quality power supply (5V 3A minimum)
- Add capacitors to stabilize power for NeoPixels
- Consider external power for high-current devices

### **2. Thermal Management**
- Use heat sinks on Raspberry Pi
- Add cooling fan for heavy loads
- Monitor CPU temperature regularly
- Implement thermal throttling if needed

### **3. Hardware Protection**
- Use appropriate resistors for LEDs
- Add diodes for inductive loads
- Implement proper grounding
- Use surge protection for power inputs

### **4. Software Practices**
- Use virtual environments
- Implement proper error handling
- Monitor system resources
- Implement logging for debugging
- Regularly update dependencies

### **5. Maintenance**
- Regular system updates
- Backup configurations
- Test hardware connections
- Monitor system health
- Clean hardware components

## 🏆 Conclusion

The Raspberry Pi setup provides a robust, dedicated platform for the WDW Monorail System with:

- **Hardware Integration**: Direct control of LEDs, displays, and sensors
- **System Monitoring**: Comprehensive health and performance tracking
- **Visual Feedback**: Status indicators and alerts
- **Reliable Operation**: Dedicated hardware for mission-critical control
- **Scalability**: Easy expansion with additional hardware

This setup transforms the WDW Monorail System into a professional-grade control platform that enhances realism, reliability, and technical sophistication.

**Enjoy your enhanced WDW Monorail System on Raspberry Pi!** 🚂🍓
