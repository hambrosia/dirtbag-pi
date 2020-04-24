"""Set up sensor and provide methods for moisture and temp reading, convert raw moisture reading to percent"""
import busio
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA

import alert_manager
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


def get_soil_moisture_percent(raw_value: int) -> float:
    """Convert raw soil moisture reading to percent """
    if raw_value == 0:
        return 0
    percent = ((raw_value - MIN_MOISTURE) / MAX_MOISTURE) * 100
    return round(percent, 2)


def check_soil_moisture_threshold() -> None:
    """Check if soil moisture in acceptable range, alert if not"""
    soil_moisture = int(get_soil_moisture_percent(get_soil_moisture()))
    min_moisture = CONFIGS['soil-moisture-alert-low']
    max_moisture = CONFIGS['soil-moisture-alert-high']
    print("min: %s, max: %s, current: %s" % (min_moisture, max_moisture, soil_moisture))
    if soil_moisture in range(min_moisture, max_moisture):
        alert_manager.send_moisture_alert_email(soil_moisture)
        print("Soil moisture is within acceptable range")
    else:
        alert_manager.send_moisture_alert_email(soil_moisture)
        print("Water your plants!")


