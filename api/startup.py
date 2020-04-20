from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import manager.db_manager as db_manager
import manager.plot_manager as plot_manager


def update_db_and_html():
    db_manager.take_and_write_reading()
    plot_manager.plot_month()

def on_startup():
    timestamp = datetime.now()
    print("%s: Prepopulating database with initial reading, prerendering index.html" % timestamp)
    # Ensure there is data in DB and an index.html on startup
    update_db_and_html()

    # Start scheduler to update DB and rerender index on interval
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_db_and_html, trigger="interval", minutes=1)
    scheduler.start()
