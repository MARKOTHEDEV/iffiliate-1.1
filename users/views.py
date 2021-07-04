# import django
from django.forms import forms
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render,redirect,HttpResponse
from django.views import generic
import requests,json
from users import models
from users import mixins as user_mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin,AccessMixin,PermissionRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from users import prepUserforPay
from django import views as django_views
from django.contrib.auth import get_user_model
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse,HttpResponseServerError
from raffleDraw import models as raffle_model




# Create your views here.

'USER DASHBOARD CODE START'


class UserDashboard(LoginRequiredMixin,user_mixins.UserHelperMixin,generic.TemplateView):

    template_name='UserDashboardPage/index.html'
    login_url ='signin'
    
    def get_context_data(self, **kwargs):
        context = super(UserDashboard, self).get_context_data(**kwargs)
        
        userEarningLimit = self.get_user_EarningLimit()
        # this is a boolean
        # check if the user is on freemode and his earnings are above 0.00 then returnTrue
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
    error_message = ''
    # this is a handler that will handle
    # listing of banks,creating of payment request,and showing of error ifsomething is wrong with account num
    # or network provideer
    userPaymentPre = prepUserforPay.UserPaymentPreparation()


    def post(self,request,*args,**kwargs):
        'this method will trigger when a user submit the file for payment Form in the front end'
        LOGINUSER = get_user_model().objects.get(email=request.user.email)
        # print(LOGINUSER)
        # print(request.POST,'Request')
        data = dict(request.POST)
        # this is a list so we access the the first item
        bankName = data['bank_name'][0]
        # account number should be numric not str
        account_number = int(data['account_number'][0])
        # we get the bank Name
        bankCode = self.userPaymentPre.get_bank_code(bankName)
        # print(bankName)
        print('--------------------')
        # print(bankCode)
        # 

        
        accountTestAndCreateRecipent = self.userPaymentPre.test_user_account(accountNumber=account_number,bankCode=bankCode,Bankname=bankName)
        # we will work with the response "accountTestAndCreateRecipent" givies us
        if accountTestAndCreateRecipent.get('status'):
            'if the status is True save data to database=> So the Admin can see it'
            # print(accountTestAndCreateRecipent)
            UserRequestPaymentModel = models.UserRequestPayment.objects.create(
                user=request.user,
                amount =  LOGINUSER.userEarnings,
                account_number=account_number,
                account_name = accountTestAndCreateRecipent['data']['name'],
                bank_code  = bankCode,
                bank_name = bankName,
                recipient_code = accountTestAndCreateRecipent['data']['recipient_code']   
            )
            # now we save it to the data base
            UserRequestPaymentModel.save()
            # after that we are Going to set the user userEarnings To Zero Since he has already requested for payment
            LOGINUSER.userEarnings = 0
            # now we save the changes
            LOGINUSER.save()
            messages.success(request,accountTestAndCreateRecipent.get('message'))
            return redirect('user-dashboard')

        else:
            # this will mean there is some kind of error
            # we will send a respose back to the front end
            messages.error(request,accountTestAndCreateRecipent.get('message'))

        # we passing listOfBanks again in the context because for some reason when the page reload it doesnt show
        return render(request, self.template_name,{'listOfBanks':self.userPaymentPre.get_available_bank_name()})
    
    
    def get_context_data(self, **kwargs):
        context = super(FileForPayment, self).get_context_data(**kwargs)
        context['listOfBanks'] = self.userPaymentPre.get_available_bank_name()
        return context
    

    def test_func(self):
        if self.isUserEligbleForPay():
          
            return True
        else:
            return False



'USER DASHBOARD CODE END'


'ADMIN USER DASHBOARD CODE START'
class AdminDashhboardIndex(user_mixins.Allow_supeusersOnly,generic.TemplateView):
    template_name='adminDashboard/index.html'
    login_url =reverse_lazy(viewname='signin')


    def get_all_the_data_to_display(self):
        'this will get all the data from the back end and return a dictionary'
        # so i got all UserRequestPayment that has not been paid
        # then create a for loop that get all the amount which i sum...

        amount_owing= int(sum([amount.amount for amount in models.UserRequestPayment.objects.filter(isPaid=False)]))
        num_of_custormers = get_user_model().objects.all().count()
        # paid users all users that are on a paid subscription
        freeMembership = models.Membership.objects.get(slug='Free')
        # this shows the paid memebership
        paid_users = models.UserMembership.objects.exclude(membership=freeMembership).count()
        # 'NOT THIS IS NOT PAYMENT MADE TO THE USER IT PAYMENT MADE TO iffiliate'
        # get the all trascation to iffiliate -> and some the amount that will give u what iffilate has made
        payment_made_to_iffiliate = int(sum([amount.amount for amount in models.PayHistory.objects.filter(who_is_getting_payed='Iffilate',paid=True)]))
    
        # get all the people that has requested for a payment
        # limit it to five
        paymentRequested = models.UserRequestPayment.objects.filter(isPaid=False)[0:5]
        # show the admin the recently created users
        # recentCreatedUser = get_user_model().objects.values_list('email').union(models.UserMembership.objects.values_list('membership__membership_type'))
        recentCreatedUser = models.UserMembership.objects.values('user__email','user__userPics','membership__membership_type')

        # print(recentCreatedUser)

        context = {
            "amount_owing":amount_owing,
            # amount_owing_percent this is what we use to calculate the visual
            # in the user interface there is a line of color that will increase according to the percentage we get here
            "amount_owing_percent":int(amount_owing/100),
            'num_of_custormers':num_of_custormers,
            'num_of_custormers_percent':int(num_of_custormers/100),
            'num_of_paid_users':paid_users,
            'num_of_paid_users_percent':int(paid_users/100),
            'payment_made_to_iffiliate':payment_made_to_iffiliate,
            'payment_made_to_iffiliate_percent':int(payment_made_to_iffiliate/100),
            'paymentRequested':paymentRequested,
            # since we dont have a date created i just reverse the list so the newset one
            # will be ontop
            'recentCreatedUser':reversed(recentCreatedUser),
        }
        return context

    
    def get_context_data(self, **kwargs):
        context = super(AdminDashhboardIndex, self).get_context_data(**kwargs)
        context.update(self.get_all_the_data_to_display())
        return context



class UserRequestPaymentListView(user_mixins.Allow_supeusersOnly,generic.ListView):
    template_name='adminDashboard/listOfpendingPayment.html'
    login_url =reverse_lazy(viewname='signin')
    model = models.UserRequestPayment
    # context_object_name = 'userpayments'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        " listOfpendingPayment = this will list all the payment that are still pending"
        context['listOfpendingPayment'] = models.UserRequestPayment.objects.filter(isPaid=False)
        return context


class BaseUserViewMixin(user_mixins.Allow_supeusersOnly):
    """
        this view avoid repeated Code in :      
                AllUserListView - that list all the user
                DeleteUserView -- that delete user
    """
    model = models.User
    login_url =reverse_lazy(viewname='signin')

class AllUserListView(BaseUserViewMixin,generic.ListView):
    "list all the users in Databse"
    template_name='adminDashboard/list_of_users.html'
    queryset =  models.User.objects.values('pk','email','userEarnings','usermembership__membership__membership_type')
    paginate_by = 10
    context_object_name = 'list_Of_All_Users'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     " listOfpendingPayment = this will list all the payment that are still pending"
    #     context['list_Of_All_Users'] = models.User.objects.values('email','userEarnings','usermembership__membership__membership_type')
    #     return context


class DeleteUserView(BaseUserViewMixin,generic.DeleteView):
    context_object_name = 'userInstance'
    template_name = 'adminDashboard/deleteUser.html'
    success_url = reverse_lazy('allUsers')



class PayUser(SingleObjectMixin,View):
    """this uses helps me work with a single object 
    #this view triggers the payment of the users
    """
    template_name ='adminDashboard/payuser.html'
    model = models.UserRequestPayment
    context_object_name = 'user_to_be_paid'

    
    def get(self,request,pk=None):
        'this just renders the template'
      

        return render(request,'adminDashboard/payuser.html',{'pk':pk,'account_name':self.get_object().account_name})

    def post(self,request,*args,**kwargs):
        'this works when the user clicks on payment button'
        # start payment proceess
        responseData = self._payUserProcesse()
        
        return render(request,'adminDashboard/payuser.html',{'pk':self.kwargs.get('pk'),
        'account_name':self.get_object().account_name,"status":responseData.get('status'),"message":responseData.get('message')})
    
    def _payUserProcesse(self):
        # the below variable is the insance of the UserRequestPayment Model we currently on
        userPaymentInstance = self.get_object()
        # print(userPaymentInstance)
        try:
            url = 'https://api.paystack.co/transfer'
            header = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "content-Type": "application/json",
            'Accept': 'application/json',}
            data = {
            "source": "balance","amount": "39800","recipient": f"{userPaymentInstance.recipient_code}",
            "reason": "Payment to Iffilate User"}
            data =json.dumps(data)
            # send the data to paystack
            resp = requests.post(url=url,data=data,headers=header)
            "this is the response data"
            respData = resp.json()

            # so this one will retunn status and message
            return respData
        except:
            return {'status':False,"message":"some error Occured Refresh the page and try Again!!"}


@csrf_exempt
def payUserWebHook(request):
    "THIS IS OFFICALLY OUR MAIN PAYSTACK WEBHOOK"
    if request.method == 'POST':
        def convert_kobo_to_naira(kobo):
            kobo = float(kobo)/100
            kobo = int(kobo)
            return kobo
        paystackResponse = json.loads(request.body)
        # print(paystackResponse)
        if paystackResponse.get('event') == 'transfer.success' and paystackResponse['data']['reason']=='Payment to Iffilate User':
            # "when we get the webhook data we check if it transfer.success or transfer.failed Then we decide to set isPaid"
            "check it this instance exits in the UserRequestPayment Table if true set it the paid true"
            "also check if the payment is payment for a user"
            if  models.UserRequestPayment.objects.filter(recipient_code=paystackResponse['data']['recipient']['recipient_code'],isPaid=False).exists():
                user_request_payment_instance = models.UserRequestPayment.objects.get(recipient_code=paystackResponse['data']['recipient']['recipient_code'],isPaid=False)
                user_request_payment_instance.isPaid=True
                user_request_payment_instance.save()
                return HttpResponse('User payment request has been paid and confirmed')
       
        if paystackResponse.get('event') == 'charge.success' and paystackResponse['data']['metadata']['custom_fields']['paymentFor'] =='raffle_game' and raffle_model.RaffleDrawPlayer.objects.filter(payment_reference=paystackResponse['data']['reference']).exists() == True:
            """this if statement is to check 
                1) if the payment was a charge.succesful=meanig the user sent money to iffliate and it was succefull
                2) also if the payment was for  raffle_game
            'then we check if the payer exist'
            """
            player = raffle_model.RaffleDrawPlayer.objects.get(payment_reference=paystackResponse['data']['reference'])
            # convert the amount from kobo to naira 
            player.amount +=convert_kobo_to_naira(paystackResponse['data']['amount'])
            player.isPayed =True
            player.save()
            return HttpResponse('User payment for raffle draw has been paid and confirmed')
            
            
    return HttpResponseServerError("something went wrong")
