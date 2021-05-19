from django.shortcuts import render,redirect
from django.views import generic
from users import models
from users import mixins as user_mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin,AccessMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from users import prepUserforPay

# Create your views here.




class UserDashboard(LoginRequiredMixin,user_mixins.UserHelperMixin,generic.TemplateView):

    template_name='UserDashboardPage/index.html'
    login_url ='signin'
    
    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        
        userEarningLimit = self.get_user_EarningLimit()
        # this is a boolean
        context['isUserEligbleForPay'] =self.isUserEligbleForPay()
        context['userEarningLimit'] = userEarningLimit
        context['userExiringDate'] = self.get_user_subExpireDate()
        # print(userEarningLimit)
        return context


class UserReadPostForMoneyPage(LoginRequiredMixin,user_mixins.RetstictFreeUser,
user_mixins.UserHelperMixin,generic.ListView):
    'so we created a mixin to retrict users that has not paid'
 
    model = models.MoneyPost
    context_object_name = 'moneyPost'
    template_name='UserDashboardPage/app-profile.html'
    login_url ='signin'
    # this attribute is comming from RetstictFreeUser
    redirect_url='pricing'

class UserReadPostForMoneyPageDetailView(LoginRequiredMixin,user_mixins.RetstictFreeUser,
user_mixins.UserHelperMixin,user_mixins.UserViewPage,generic.DetailView):

    model = models.MoneyPost
    context_object_name = 'post'

    template_name='UserDashboardPage/post-details.html'
    login_url ='signin'
    # this attribute is comming from RetstictFreeUser
    redirect_url='pricing'


class UserTransactionPage(LoginRequiredMixin,user_mixins.UserHelperMixin,generic.ListView):
    template_name='UserDashboardPage/userTransaction.html'
    login_url ='signin'
    model = models.PayHistory
    context_object_name ='paymentHistoryForMembership'
    paginate_by =5

    
    def get_context_data(self, **kwargs):
        context = super(UserTransactionPage, self).get_context_data(**kwargs)
        userEarningLimit = self.get_user_EarningLimit()
        
        context['userExiringDate'] = self.get_user_subExpireDate()
        # print(userEarningLimit)
        return context



class FileForPayment(LoginRequiredMixin,UserPassesTestMixin,user_mixins.UserHelperMixin,generic.TemplateView):
    """
        this is a view that help to rigister Eligble user for payment it adds them to the
        UserRequestPayment which will make user Admin see the user request and he will approve
    """
    """
    # this is the first process to get payed u will have to file for a payment 
    # that if u are Eligble"""
    template_name = 'UserDashboardPage/queUserpayment.html'
    userPaymentPre = prepUserforPay.UserPaymentPreparation()

    
    
    def get_context_data(self, **kwargs):
        context = super(FileForPayment, self).get_context_data(**kwargs)
        context['listOfBanks'] = self.userPaymentPre.get_available_bank_name()
        return context
    

    def test_func(self):
        if self.isUserEligbleForPay():
          
            return True
        else:
            return False