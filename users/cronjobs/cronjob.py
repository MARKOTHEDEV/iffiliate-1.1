from apscheduler.schedulers.background import BackgroundScheduler
from users import models
from .checkUserStatus import UserStatusChecker

def start():
    'this function start the task when it runs'
    scheduler = BackgroundScheduler()
    userChecker = UserStatusChecker()
    
    # scheduler.add_job(userChecker.start,"interval",minutes=1,id="MoneyPost_001",replace_existing=True)
    scheduler.add_job(userChecker.start,"interval",hours=1,id="checkExpiredSub_001",replace_existing=True)
    scheduler.start()
    




def createMoneyPost():
    moneyPost = models.MoneyPost.objects.create(title='Hey was created by CronJob',content="Yo What up")
    moneyPost.save()




# me = UserStatusChecker()
# me.start()