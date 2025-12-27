from setuptools import setup, find_packages

setup(
    name="wdw-sensors",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Adafruit_DHT==1.4.0",
        "smbus2==0.4.1",
        "pigpio==1.78",
    ],
    author="WDW Monorail System",
    description="WDW Monorail Sensors Library",
    license="MIT",
    keywords="sensors raspberrypi wdw monorail",
    url="https://github.com/wdw-monorail/wdw-sensors",
)
