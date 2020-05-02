"""Prepopulate database, prerender html, start scheduler"""
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import config.config as config
import manager.sensor_manager as sensor_manager
import manager.request_manager as request_manager

CONFIGS = config.get_configs()
SCHEDULER = BlockingScheduler()

def take_and_post_reading():
    """Get sensor ID and Name from configs, take soil reading, pass to request manager"""
    timestamp = str(datetime.now())
    sensor_id = CONFIGS['sensor-id']
    sensor_name = CONFIGS['sensor-name']
    soil_moisture = sensor_manager.get_soil_moisture()
    soil_temp = sensor_manager.get_soil_temp()
    
    response = request_manager.post_reading(
            timestamp=timestamp,
            sensor_id=sensor_id,
            sensor_name=sensor_name,
            soil_moisture=soil_moisture,
            soil_temp=soil_temp
            )


def configure_reading_job():
    """Configure scheduler to take reading"""
    polling_interval = CONFIGS['polling-interval-minutes']
    SCHEDULER.add_job(func=take_and_post_reading, trigger='interval', minutes=polling_interval)

    timestamp = datetime.now()
    print("%s: Scheduler configured to take and save reading every %i minutes" % (timestamp, polling_interval))


def on_startup():
    """Take a reading, start scheduler"""
    timestamp = datetime.now()
    print("%s: Sending first reading and configuring scheduler." % timestamp)
    
    # Take and send reading on startup
    take_and_post_reading()
    
    # Start scheduler
    configure_reading_job()
    try:
        SCHEDULER.start()
    except (KeyboardInterrupt, SystemExit):
        pass
