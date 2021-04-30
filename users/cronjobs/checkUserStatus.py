# this module check every user in the sytem and change them to free if they expire
# every night
from users import models
from django.contrib.auth import get_user_model
import datetime
"""
Steps

    Get all the users the loop them
    for each of the user we get their expiring date if user is a free user we skip him
    else we check if thier expiring date is GREATER OR EQUAL TO TODAY


today:2021-05-01
"""

class UserStatusChecker:

    def __init__(self):
        self.freemembership =  models.Membership.objects.get(slug='Free') 

    
    def get_user_expiring_date(self,user):
        'returns true if user has expired'
        currentUserMembership =  models.UserMembership.objects.get(user=user)
        subObject = models.Subscription.objects.get(user_membership=currentUserMembership)


        subscriptionExpireDateStr = datetime.datetime.strftime(subObject.expires_in,'%y-%m-%d')
        # all i did was to parse the todayStr to a date object
        userSubExpireDate = datetime.datetime.strptime(subscriptionExpireDateStr,'%y-%m-%d')


        todayStr = datetime.datetime.strftime(datetime.datetime.now(),'%y-%m-%d')
        # all i did was to parse the todayStr to a date object
        todayDate = datetime.datetime.strptime(todayStr,'%y-%m-%d')
        # print('None has expired')

        if userSubExpireDate >= todayDate:
            'then his sub is log over due make him a free user'
            self.setUser_To_Free_Mode(currentUserMembership)

            return True
        else:
            return False

    def setUser_To_Free_Mode(self,user_membership):
        'this method will turn a user subscription to free account'
        # print({'user formaer membershipt:':user_membership.membership,'username':user_membership.user})
        user_membership.membership = self.freemembership
        
        user_membership.save()

    def check_userMembership_sub_if_it_free_mode(self,user):
        'this method is used to check if the user is a free mode user'
        isUser_membershipFree = models.UserMembership.objects.filter(user=user,membership=self.freemembership).exists()

        return isUser_membershipFree


    def start(self):
        allUsers = get_user_model().objects.all()
        
        for user in allUsers:

            if self.check_userMembership_sub_if_it_free_mode(user=user) == False:
                'this condition checks if the user is not a freeMember'
                
                """
                this function get and check the expiring date if it expired it 
                calls the self.setUser_To_Free_Mode(self,user_membership) and set the current user membershipt to free"""
                print('CronTab Started:')
                self.get_user_expiring_date(user)#this funtion get the  

