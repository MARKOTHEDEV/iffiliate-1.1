import datetime
from django.http.response import HttpResponseRedirect
from django.shortcuts import (render,redirect)
from django.urls import reverse
import requests,json
from django.views.generic import (View,ListView,FormView,TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from . import form as customforms
from . import (models,mixins)
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
# print(models.RaffleDrawPlayer.get_all_winners())


# def registerFor_RaffleDraw(request):
#     'this renders a form that takes user amount and account mostly usefull deails'

# ,mixins.AllowPlayer_If_It_TimeForRaffleDraw
class registerFor_RaffleDraw(LoginRequiredMixin,FormView):
    "dont forget to put in the correct call back"
    form_class = customforms.raffleRegisterForm
    template_name = 'raffleDraw/registerForGame.html'
    login_url = 'home'
    # dont forget to use the backslash

    def check_if_it_time_for_game(self):
        currentGame = models.RaffleDrawBatch.objects.get(is_close=False)
        currentGameDate = mixins._format_django_date_to_pythondate(currentGame.when)
        if_it_time_forEvent = datetime.datetime.now() >= currentGameDate
        return if_it_time_forEvent


    def dispatch(self, request, *args, **kwargs):
        print(self.check_if_it_time_for_game())
        if self.check_if_it_time_for_game() == False:
            return redirect('countDown')
        return super(registerFor_RaffleDraw, self).dispatch(request, *args, **kwargs)
    
  
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
        


def countDown(request):
    'this view shows our nice countdown to the game'
    currentGame = models.RaffleDrawBatch.objects.get(is_close=False)
    print(currentGame.when)
    return render(request,'raffleDraw/countDown.html',{'gameDate':currentGame.when})

@csrf_exempt
def raffleDraw_callback(request):
    'THIS will just render the users a info page our webhook will handle the verfication of the payment'
    return render(request,'raffleDraw/paymentInfo.html')

# @api_view(['GET',])
# def check_batchDate(request):
#     # this is to check if it time for a mae or  not -- if it true redirect the user to the payment page
#     today = datetime.datetime.now()
#     # the mixin
#     currentGame = models.RaffleDrawBatch.objects.get(is_close=False)
#     currentGameDate = mixins.AllowPlayer_If_It_TimeForRaffleDraw()._format_rafflewhen(currentGame.when)
#     is_event = datetime.datetime.now() >= currentGameDate

#     return Response({'ss':'Hey i recived the response','currentGame':currentGame.when,'is_event':is_event})




