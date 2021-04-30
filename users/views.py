from django.shortcuts import render,redirect
from django.views import generic
from users import models
from users import mixins as user_mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin,AccessMixin
from django.contrib import messages

# Create your views here.




class UserDashboard(LoginRequiredMixin,user_mixins.UserHelperMixin,generic.TemplateView):

    template_name='UserDashboardPage/index.html'
    login_url ='signin'
    
    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)

        userEarningLimit = self.get_user_EarningLimit()
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

# 
    

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
