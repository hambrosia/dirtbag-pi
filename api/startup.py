"""Prepopulate database, prerender html, start scheduler"""
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import config.config as config
import manager.db_manager as db_manager
import manager.plot_manager as plot_manager


def update_db_and_html():
    """Takes a reading, writes it to the database, updates the graph"""

    db_manager.take_and_write_reading()
    plot_manager.plot_month()

def on_startup():
    """Prepopulate database, prerender html, start scheduler"""

    timestamp = datetime.now()
    print("%s: Prepopulating database with initial reading, prerendering index.html" % timestamp)
    # Ensure there is data in DB and an index.html on startup
    update_db_and_html()

    # Start scheduler to update DB and rerender index on interval
    polling_interval = config.get_configs()['polling-interval-minutes']
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_db_and_html, trigger="interval", minutes=polling_interval)
    scheduler.start()
    timestamp = datetime.now()
    print("%s: Scheduler configured to take and save reading every %i minutes" % (timestamp, polling_interval))
