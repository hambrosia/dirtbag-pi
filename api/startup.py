"""Prepopulate database, prerender html, start scheduler"""
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import config.config as config
import manager.db_manager as db_manager
import manager.plot_manager as plot_manager
from manager.sensor_manager import check_soil_moisture_threshold as check_threshold

CONFIGS = config.get_configs()
SCHEDULER  = BackgroundScheduler()
def update_db_and_html():
    """Takes a reading, writes it to the database, updates the graph"""
    db_manager.take_and_write_reading()
    plot_manager.plot_month()


def start_monitor():
    """ Start scheduler to update DB and rerender index on interval"""
    polling_interval = CONFIGS['polling-interval-minutes']
    SCHEDULER.add_job(func=update_db_and_html, trigger='interval', minutes=polling_interval)
    
    timestamp = datetime.now()
    print("%s: Scheduler configured to take and save reading every %i minutes" % (timestamp, polling_interval))


def start_threshold_alert():
    alert_time = CONFIGS['soil-moisture-alert-time']
    alert_hour = alert_time.split(":")[0]
    alert_minute = alert_time.split(":")[1]
    SCHEDULER.add_job(func=check_threshold, trigger='cron', hour='18', minute='12')


def on_startup():
    """Prepopulate database, prerender html, start scheduler"""
    timestamp = datetime.now()
    print("%s: Prepopulating database with initial reading, prerendering index.html" % timestamp)
    
    # Ensure there is data in DB and an index.html on startup
    update_db_and_html()
    
    # Start monitor scheduler
    start_monitor()
    
    #Start alert scheduler
    start_threshold_alert() 
    
    SCHEDULER.start() 
