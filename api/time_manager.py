from datetime import timedelta
from datetime import datetime

# Prepare intervals for average calculations
def get_timestamp_24_hrs_ago():
    day_delta = timedelta(hours = 24)
    return datetime.now() - day_delta

def get_timestamp_week_ago():
    week_delta = timedelta(days = 7)
    return datetime.now() - week_delta

def get_timestamp_month_ago():
    month_delta = timedelta(months = 1)
    return datetime.now() - month_delta

