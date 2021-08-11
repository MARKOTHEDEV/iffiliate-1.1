"""
this module is to pay user that logged in 

    we need to check if the user logged in date is same with the Todays date:
        it true we pay accordim
        paidUser  = get all user membership that are not free using .values('user','membership__slug')
        now that we have each user membeship type we can pay the appropraitly
"""
import datetime 
from django.db.models import Q
from django.contrib.auth import get_user_model
from users.models import Membership,UserMembership

# E.G 14th
TODAYS_DAY = datetime.datetime.now().day

def start():
    free_membership = Membership.objects.get(slug='Free')
    """
        paidUsers conatians a list of  all users that belongs to a 
        1)Paid plan
        2)a dictonary of the user last_login whichis a datetime object and the user Current membership
        ~Q(membership=free_membership) -- means ~ nOt
    """
    paidUsers = list(UserMembership.objects.filter(~Q(membership=free_membership)).values('user','user__last_login','membership__slug'))
  
    for userObj in paidUsers:
        user  = get_user_model().objects.get(id=userObj.get('user'))
        if userObj.get('membership__slug') == 'Bronze' and userObj.get('user__last_login').day == TODAYS_DAY:
            user.userEarnings = 430
 


        if userObj.get('membership__slug') == 'Gold' and userObj.get('user__last_login').day == TODAYS_DAY:
            user.userEarnings = 900

        if userObj.get('membership__slug') == 'Silver' and userObj.get('user__last_login').day == TODAYS_DAY:
            user.userEarnings = 600

        # we have to save changes 
        user.save()
