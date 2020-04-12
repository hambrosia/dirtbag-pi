# Dirtbag-Pi

## Overview
Dirtbag Pi is a network-connected garden and plant monitor written in Python for Raspberry Pi. It takes soil moisture and temperature readings using a widely available capacative sensor and makes them available through a simple webpage on the local network.

## Installation and Requirements
* Use an [Adafruit STEMMA Soil Sensor](https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test)
* Connect the sensor to the [proper pins](https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test).
    * Pi 3V3 to sensor VIN
    * Pi GND to sensor GND
    * Pi SCL to Sensor SCL
    * Pi SDA to sensor SDA
* Enable I2C on the Raspberry Pi: `sudo raspi-config` then select interfaces, followed by I2C. Select `Enable` and exit.
* Raspberry Pi should also have `pip3` installed: `sudo apt-get install python3-pip`
* Install the requirements: `pip3 install -r requirements.txt`
* Get the IP of your Raspberry Pi: `ip addr`
* Start the Flask application: `python3 api.py`
* Navigate to `http://<ip-addr-of-pi>:5000` and the soil moisture and soil temperature readings will be shown.

## Understanding the Output
* Soil capacitance readings are returned by the sensor as a value between ~315 (air) and ~1015 (submersion in water). DirtBag converts this raw capacitance reading to an approximate moisture percent value rounded to two decimal points. 
* Soil temperature readings are returned natively in Celcius by the sensor and displayed to the user in Celcius.

## Current and Planned Features
* Part 1(DONE): Displays a webpage on the local network that shows the soil moisture and tempoerature.
* Part 2: The webpage displays historical data including graphs and averages that persist on reboot of the Raspberry Pi.
* Part 3: Anomaly alerting on unusual changes in moisture or temperature.
