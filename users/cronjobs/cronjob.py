from apscheduler.schedulers.background import BackgroundScheduler
from users import models
from .checkUserStatus import UserStatusChecker
from .NewsGetterAndSaver import runScraper

def start():
    'this function start the task when it runs'
    scheduler = BackgroundScheduler()
    userChecker = UserStatusChecker()
    
    scheduler.add_job(runScraper,"interval",hours=24,id="MoneyPost_001",replace_existing=True)
    scheduler.add_job(userChecker.start,"interval",hours=23,id="checkExpiredSub_001",replace_existing=True)
    # scheduler.start()
    







# me = UserStatusChecker()
# me.start()