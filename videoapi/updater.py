from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from videoapi.utils import update_data


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_data, "interval", seconds=20)
    scheduler.start()
