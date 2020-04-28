"""Create timestamps for use in database queries over 24 hrs, one week, and one month """
from datetime import datetime, timedelta


# Prepare intervals for average calculations
def get_timestamp_24_hr_ago():
    """Return a timestamp 24 hours prior to the present time"""
    day_delta = timedelta(hours=24)
    return datetime.now() - day_delta


def get_timestamp_week_ago():
    """Return a timestamp seven days prior to the present time"""
    week_delta = timedelta(days=7)
    return datetime.now() - week_delta


def get_timestamp_month_ago():
    """Return a timestamp 31 days prior to the present time"""
    month_delta = timedelta(days=31)
    return datetime.now() - month_delta
