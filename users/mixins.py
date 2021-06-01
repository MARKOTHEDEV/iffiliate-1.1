from users import models
from django.contrib.auth.mixins import AccessMixin,UserPassesTestMixin
from users import models
from django.contrib import messages
from django.shortcuts import redirect
from  . import signals
import datetime
from django.contrib.auth import get_user_model

class UserHelperMixin:
    'This a mixin that will contain helper methods that helps the user model provide ansers out of the box'
    

    def get_user_EarningLimit(self):
        'this mthod gives u the user earning limit'
        'this method returns the user earning limit'
        user= self.request.user
        currentUserMembership =  models.UserMembership.objects.get(user=user)

        return currentUserMembership.membership.earningLimit

    
    def get_user_subExpireDate(self):
        'this get the current user expiring day it returns the actual date'
        currentUserMembership =  models.UserMembership.objects.get(user=self.request.user)
        subObject = models.Subscription.objects.get(user_membership=currentUserMembership)
        return subObject.expires_in

    def isUserEligbleForPay(self):
        membership = models.Membership.objects.get(slug ='Free')
        user=  get_user_model().objects.get(email=self.request.user)
        currentUserMembership =  models.UserMembership.objects.get(user=user)
        # check if the user is on freemode and his earnings are above 0.00 then returnTrue
        if membership.membership_type == currentUserMembership.membership.membership_type and user.userEarnings > 0.00:
            return True
        else:
            return False



class RetstictFreeUser(AccessMixin):
    "This mixins is to retrict the action of the Free users "

    error_message = 'You Need a Paid Account to Start Your Earnings'
    # this attribute redirect the free user
    redirect_url=''
    # first get the user object and save it globally
    # check if user is on free return boolean depending on that 
    # send a custom message and redirect the user



    def dispatch(self, request, *args, **kwargs):
    
        membership = models.Membership.objects.get(slug ='Free')
        user= self.request.user
        currentUserMembership =  models.UserMembership.objects.get(user=user)

        if membership.membership_type == currentUserMembership.membership.membership_type:
            # print('redirect THis broke ass nigga')
            return self.redirect_free_user()
        
        # print('dont redirect this broke ass niga')


        return super(RetstictFreeUser, self).dispatch(request, *args, **kwargs)

    def redirect_free_user(self):
        'send message to the user and redirect the user'
        messages.warning(self.request,self.error_message)

        return redirect(self.redirect_url)

class UserViewPage:
    'this mixin trigars when u see a model detail page'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

        except  self.Model.DoesNotExist:
            instance =None

        if request.user.is_authenticated and instance is not None:
            signals.object_viewed_signal.send(instance.__class__,instance=instance,request=request) 
        
        return super(UserViewPage, self).dispatch(request, *args, **kwargs)


class Allow_supeusersOnly(UserPassesTestMixin) :
    def test_func(self):
        'we check if the user is a staff if true then let them in else show them that this page is forbidden'
        return self.request.user.is_staff