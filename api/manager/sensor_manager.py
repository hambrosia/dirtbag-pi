"""Set up sensor and provide methods for moisture and temp reading, convert raw moisture reading to percent"""
import busio
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA

import config.config as config


# Sensor setup
I2C = busio.I2C(SCL, SDA)
SS = Seesaw(I2C, addr=0x36)

# Soil reading calibration
MIN_MOISTURE = config.get_configs()['soil-moisture-min']
MAX_MOISTURE = config.get_configs()['soil-moisture-max'] - MIN_MOISTURE

def get_soil_moisture():
    """Return soil moisture reading"""
    return SS.moisture_read()


def get_soil_temp():
    """Return soil temp in Celcius"""
    return round(SS.get_temp(), 2)


def get_soil_moisture_percent(raw_value: int) -> float:
    """Convert raw soil moisture reading to percent """
    if raw_value == 0:
        return 0
    percent = ((raw_value - MIN_MOISTURE) / MAX_MOISTURE) * 100
    return round(percent, 2)
