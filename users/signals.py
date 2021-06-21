from users import  models
from datetime import datetime as dt
from datetime import timedelta
import datetime
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from  allauth.account.signals  import user_signed_up
from django.contrib.auth import get_user_model


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

@receiver(user_signed_up)
def give_socialUser_freeMode(sender,request, user,**kwargs):
    """
        this function does the same job that users.serializers.UserSerializers.create method  does
        since this is a new user he has to have a free membership first
        before he can purchase a paid membership
        #NOTE THIS SIGNAL IS FOR GOOGLE AUTH USERS!!
    """

    Freesub = models.Membership.objects.get(membership_type='Free')
    user_membership = models.UserMembership.objects.create(user=user,membership=Freesub)
    # print("successfully create a user using django allauth signals")


from django.dispatch import Signal


object_viewed_signal  = Signal(providing_args=['instance','request'])


