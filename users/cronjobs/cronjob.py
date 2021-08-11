from apscheduler.schedulers.background import BackgroundScheduler
from users import models
from .checkUserStatus import UserStatusChecker
from .NewsGetterAndSaver import runScraper
from .Api_Post import NEWS
# from .chooseRaffleDraw_winner import chooseRaffleDraw_winner_randomly
from . import payUser_onlogin


def start():
    'this function start the task when it runs'
    scheduler = BackgroundScheduler()
    userChecker = UserStatusChecker()
    
    print("Loading Scheduler.....")
    # scheduler.add_job(runScraper,"interval",hours=24,id="MoneyPost_001",replace_existing=True)
    # scheduler.add_job(userChecker.start,"interval",hours=23,id="checkExpiredSub_001",replace_existing=True)
    scheduler.add_job(payUser_onlogin.start,"interval",hours=4,id="payUser_onlogin_001",replace_existing=True)
    scheduler.add_job(NEWS.run,"interval",hours=5,id="get_money_post_002",replace_existing=True)
    
    
    scheduler.start()
    





# me = UserStatusChecker()
# me.start()