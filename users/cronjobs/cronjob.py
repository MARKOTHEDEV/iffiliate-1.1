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
    "every 19 hours  Check if the user Sub Has Expired"
    scheduler.add_job(userChecker.start,"interval",hours=19,id="checkExpiredSub_001",replace_existing=True)

    "every 23 hours  if user has logged in for that day and pay them"
    scheduler.add_job(payUser_onlogin.start,"interval",hours=23,id="payUser_onlogin_001",replace_existing=True)
    "every 24 hours  Get News Articles So USers can Earn"
    scheduler.add_job(NEWS.run,"interval",hours=24,id="get_money_post_002",replace_existing=True)
    
    
    scheduler.start()
    





# me = UserStatusChecker()
# me.start()