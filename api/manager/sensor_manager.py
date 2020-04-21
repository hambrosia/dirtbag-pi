import busio
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA

# Sensor setup
I2C = busio.I2C(SCL, SDA)
SS = Seesaw(I2C, addr=0x36)

# Soil reading calibration
MIN_MOISTURE = 315
MAX_MOISTURE = 1015 - MIN_MOISTURE

def get_soil_moisture():
    return SS.moisture_read()

def get_soil_temp():
    return round(SS.get_temp(), 2)

# Convert raw moisture reading to percent
def get_soil_moisture_percent(raw_value: int) -> float:
    if raw_value == 0:
        return 0
    percent = ((raw_value - MIN_MOISTURE) / MAX_MOISTURE) * 100
    return round(percent, 2)
