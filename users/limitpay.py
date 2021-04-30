# this models is from users
from . import models
from django.contrib.auth import get_user_model





def LimitUserPay(userEmail):
    'this function checks the current user limit if his pay is equal or above the pay re assign the pay to his limit'

    
    user = models.User.objects.get(email=userEmail)
    usermembership = models.UserMembership.objects.get(user=user)
    # now that we  have gotten the user membership we will check the limit
    memebership = models.Membership.objects.get(membership_type=usermembership.membership)

    print('user Earning:',user.userEarnings)
    print('user Limit:',memebership.earningLimit)
    if user.userEarnings >= memebership.earningLimit:
        user.userEarnings = memebership.earningLimit
        user.save()
        # this means the user has reach his limit dont give
        # him or her chance to earn more
