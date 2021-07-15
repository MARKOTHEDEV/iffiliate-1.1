import datetime
from django.db.models.base import Model
from django.http.response import HttpResponseRedirect
from django.shortcuts import (render,redirect)
from django.urls import reverse,reverse_lazy
import requests,json
from django.views.generic import (View,ListView,FormView,TemplateView,DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from . import form as customforms
from . import (models,mixins)
from users import mixins as user_mixins



# Create your views here.
# print(models.RaffleDrawPlayer.get_all_winners())


# def registerFor_RaffleDraw(request):
#     'this renders a form that takes user amount and account mostly usefull deails'

# ,mixins.AllowPlayer_If_It_TimeForRaffleDraw
class registerFor_RaffleDraw(mixins.CheckGame,FormView):
    "dont forget to put in the correct call back"
    form_class = customforms.raffleRegisterForm
    template_name = 'raffleDraw/registerForGame.html'

    # dont forget to use the backslash

 
 
    def form_valid(self,form):
        'this is the amount the user decides to pay'
        amount = form.cleaned_data['amount']
      
        response = self._Initialize_payment(amount,self.request.user.email)
        if response['status'] == True:
            # then the request was good we gonna take the person to paystack payment getway
            # so the user can pay
            "since the person has started the payment proccess let check if there is a batch that is open"
            raffle_batch = models.RaffleDrawBatch.objects.get(is_close=False)
            "then we create a player ... and add that player to a BAtch"
            player,isPlayercreated = models.RaffleDrawPlayer.objects.get_or_create(
                    user = self.request.user,
                    raffle_draw_batch= raffle_batch,
                    # amount = amount,
                    # payment_reference =response['reference']
                    )
            player.payment_reference = response['reference'] 

            player.save()
            return HttpResponseRedirect(response['paystacklink'])
        else:
            # the person had some error then tak the person to the error page
            messages.success(self.request,response['message'])
            return redirect('errorpage')
        # return render(request,'raffleDraw/registerForGame.html')

    
    def _Initialize_payment(self,amount,email):
        # convert it to NGN
        amount = float(amount)*100
        amount = int(amount)
        url ='https://api.paystack.co/transaction/initialize'
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email":email, "amount":amount,
            'currency':'NGN',
            "metadata":{
                "custom_fields":{"paymentFor":'raffle_game'}
            },
            # we overriding our THE call back we specified in our call back
            "callback_url":settings.RAFFLE_DRAW_PAYMENT_CALLBACK_URL,
            
        }
        try:
            response  = requests.post(url,data=json.dumps(data),headers=headers)
            # respData is the data pay stack returns to us
            respData = response.json()
            if respData['status'] == True and response.status_code == 200:
                return {'status':True,'message':respData['message'],
                'paystacklink':respData['data']['authorization_url'],'reference':respData['data']['reference']}
            else:
                return {'status':False,'message':respData['message']}
        except requests.exceptions.ConnectionError:
            return {'status':False,'message':'Network Problem'}
        




def Game_is_close_for_now(request):

    return render(request,'raffleDraw/noGame.html')


"The view Below Are Will Show In the Custom  Admin Dashboard"

class ListOfRaffleDraw(user_mixins.Allow_supeusersOnly,ListView):
    login_url = reverse_lazy(viewname='signin')
    'this list all the availble RaffleDraw in the database'
    model = models.RaffleDrawBatch
    template_name = 'adminDashboard/ListOfRaffleDraw.html'
    context_object_name = 'ListOfRaffleDraw'

    def get_queryset(self):
        "We ordering by the is_close column--> THe New RaffleBatch Will Be At The Top"
        return models.RaffleDrawBatch.objects.all().order_by('is_close')



class RaffleDrawDetail(user_mixins.Allow_supeusersOnly,DetailView):
    login_url = reverse_lazy(viewname='signin')
    model = models.RaffleDrawBatch
    template_name = 'adminDashboard/RaffleDrawDetail.html'
    context_object_name = 'raffledraw'

    def get_context_data(self, **kwargs):
        context  = super().get_context_data(**kwargs)
        # self.get_object() returns the instance of the current RaffleBatch We viewing
        context['listOfPlayer'] = models.RaffleDrawPlayer.objects.filter(raffle_draw_batch=self.get_object())
  
        return context