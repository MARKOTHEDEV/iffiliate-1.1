from users import  models
from datetime import datetime as dt
from datetime import timedelta
import datetime
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


today = datetime.date.today()
# print(today)




@receiver(post_save, sender=models.UserMembership)
def create_subscription(sender, instance,created, *args, **kwargs):
    'WHEN UserMembership is created create a subcription'
    # user = models.UserMembership
    
    if created:
        'if the instance is was just created then create a sub for him'
        models.Subscription.objects.create(user_membership=instance, expires_in=dt.now().date() + timedelta(days=instance.membership.duration))
    else:
        'if the UserMembership-instace was created before just update the the sub'
        # print()
        sub,created = models.Subscription.objects.get_or_create(user_membership=instance)
        sub.expires_in = dt.now()
        sub.expires_in = dt.now().date() + timedelta(days=instance.membership.duration)
        sub.save()

        # sub.delete()



from django.dispatch import Signal


object_viewed_signal  = Signal(providing_args=['instance','request'])


