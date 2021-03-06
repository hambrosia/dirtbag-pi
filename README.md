# DirtBag Pi

## Overview
DirtBag Pi is a network-connected garden and plant monitor written in Python for Raspberry Pi. It takes soil moisture and temperature readings using a widely available capacative sensor and makes them accessible through a simple webpage on the local network.

![DirtBag Pi](img/dbp.jpg?raw=true "DirtBag Pi")

## Installation and Requirements (Cloud-Hosted)
The cloud-hosted implementation of DirtBag Pi aims to make the garden monitor information available over the internet as well as reduce the complexity and computing needs of the sensor client. In this model, the sensor is only responsible for taking soil readings. These readings are sent to a Lambda to be validated and stored in DynamoDB. Dynamo triggers another Lambda on any changes, which renders the HTML graph and saves it to a public S3 bucket.
![Cloud-hosted implementation](img/cloud.png?raw=true "Cloud-hosted implementation")

To set up the cloud-hosted version of DirtBag Pi follow the steps below.
* Deploy the Terraform manifest to AWS
    * Copy `secret_vars_template.txt` to `secret_vars.tf` and update with your AWS account number.
    * Create a workspace, e.g. `terraform workspace new dirtbag-us-east-2`
    * Use `zip_lambdas.sh` and `make_layer.sh` scripts to zip the Lambda functions and layers.
    * Terraform `apply` into the newly created workspace.
    * Save the client keys and the index URL
* Set up the client on the Raspberry Pi
    * Follow the first five steps from the self-hosted guide to set up the sensor on the Raspberry Pi.
    * Copy the client application to the Pi using either `scp` or `git clone`
    * In the home folder of the Pi, create the `.aws/credentials` and `.aws/config` files
    * `.aws/credentials` 
      ```
      [default]
      aws_access_key_id=AKIAIOSFODNN7EXAMPLE
      aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
      ```
      `.aws/config`
      ```
      [default]
      region=us-east-2
      output=json
      ```
    * Navigate to `config/config.json` and update the `sensor-id` and `sensor-name` fields to your preferred choices.
    * In the root project folder create a virtual environment `python3 -m venv venv`
    * Install the requirements `pip3 install -r requirements.txt`
    * Run the application using nohup `nohup python3 app/app.py &` 
* Confirm it all works by navigating to the index URL that was output during the Terraform apply. You should see a graph of soil moisture and temperature readings, however it will only have one value since the application just started recording readings. 

## Installation and Requirements (Self-Hosted)
* Use an [Adafruit STEMMA Soil Sensor](https://www.adafruit.com/product/4026)
* Connect the sensor to the [proper pins](https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor/python-circuitpython-test).
    * Pi 3V3 to sensor VIN
    * Pi GND to sensor GND
    * Pi SCL to Sensor SCL
    * Pi SDA to sensor SDA
* Enable I2C on the Raspberry Pi: `sudo raspi-config` then select interfaces, followed by I2C. Select `Enable` and exit.
* Raspberry Pi should also have `pip3` installed: `sudo apt-get install python3-pip`
* Install the requirements: `pip3 install -r requirements.txt`
* Setup the Postgres database
    * Assume the root postgres user `sudo su postgres`
    * Create a user for the pi (or your current username) `createuser pi -P --interactive;`
    * Create a database called dirtbag `create database dirtbag;`
    * Create a table caleld readings `create table readings(uuid uuid, timestamp timestamp, soilmoisture float, soiltemp float);`
    * Grant the user you created (pi) privileges to modify the database `GRANT ALL PRIVILEGES ON DATABASE dirtbag TO pi;`
* Copy the secrets template, e.g. `cp api/config/secret-template.json api/config/secret.json` and populate with the correct database configuration based on the last step as well as e-mail account, password, and SMTP settings. `secret.json` is ignored by default, but exercise caution and carefully review your commits to ensure no secrets are published to your version control platform.
* Get the IP of your Raspberry Pi: `ip addr`
* Start the Flask application: `python3 api.py`
* Navigate to `http://<ip-addr-of-pi>:5000` and the soil moisture and soil temperature readings will be shown.
* To leave DirtBag running after the SSH session with the Raspberry Pi ends, use `nohup`. For example `nohup python3 app.py &` will allow for termination of the SSH session while leaving DirtBag Pi running so data collection and threshold alerting uninterrupted.  
 
## Understanding the Output
* Soil capacitance readings are returned by the sensor as a value between 200 and 2000. In practice, the raw readings range between ~315 (exposure to fresh Los Angeles air) and ~1015 (submersion in tap water). DirtBag converts the raw capacitance reading to an approximate moisture percent value calibrated for LA air and water and rounded to two decimal points.
* Soil temperature readings are returned natively by the sensor in Celsius and displayed to the user in Celsius.
![Example plot](img/graph_browser.png?raw=true "Example Graph")

## Current and Planned Features
* Part 1 (DONE): Displays a webpage on the local network that shows the soil moisture and temperature.
* Part 2 (DONE): The webpage displays historical data including graphs and averages that persist on reboot of the Raspberry Pi.
* Part 3 (DONE): Threshold alerting to send an email if moisture readings are outside of a specified range.
* Part 4 (DONE): Split sensor client from webserver and database. Host the database and webpage in the cloud.
* Part 5: Support for multiple sensor clients with unique sensor IDs.
