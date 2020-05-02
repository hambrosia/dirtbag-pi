"""Set up sensor and provide methods for moisture and temp reading, convert raw moisture reading to percent"""
import busio
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA

import config.config as config

# Sensor setup
I2C = busio.I2C(SCL, SDA)
SS = Seesaw(I2C, addr=0x36)

CONFIGS = config.get_configs()

# Soil reading calibration
MIN_MOISTURE = CONFIGS['soil-moisture-min']
MAX_MOISTURE = CONFIGS['soil-moisture-max'] - MIN_MOISTURE


def get_soil_moisture():
    """Return soil moisture reading"""
    return SS.moisture_read()


def get_soil_temp():
    """Return soil temp in Celsius"""
    return round(SS.get_temp(), 2)

