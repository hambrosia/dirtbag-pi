"""Prepopulate database, prerender html, start scheduler"""
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import config.config as config

CONFIGS = config.get_configs()
SCHEDULER = BackgroundScheduler()


def start_monitor():
    """ Start scheduler to update DB and rerender index on interval"""
    polling_interval = CONFIGS['polling-interval-minutes']
#    SCHEDULER.add_job(func="", trigger='interval', minutes=polling_interval)

    timestamp = datetime.now()
    print("%s: Scheduler configured to take and save reading every %i minutes" % (timestamp, polling_interval))


def on_startup():
    """Validate config.json and connection to API, take a reading, start scheduler"""
    timestamp = datetime.now()
    print("%s: Validating config.json and cnonection to API." % timestamp)
    
    # Start monitor scheduler
#    start_monitor()
#    SCHEDULER.start()
