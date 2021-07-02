from django.http.response import HttpResponseRedirect
from django.shortcuts import (render,redirect)
from django.urls import reverse
import requests,json
from django.views.generic import (View,TemplateView,FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from . import form as customforms
from . import models
from django.views.decorators.csrf import csrf_exempt

# Create your views here.



# def registerFor_RaffleDraw(request):
#     'this renders a form that takes user amount and account mostly usefull deails'

class registerFor_RaffleDraw(LoginRequiredMixin,FormView):
    "dont forget to put in the correct call back"
    form_class = customforms.raffleRegisterForm
    template_name = 'raffleDraw/registerForGame.html'
    login_url = 'home'
    # dont forget to use the backslash
  
    def form_valid(self,form):
        'this is the amount the user decides to pay'
        amount = form.cleaned_data['amount']
        print(self.request.user.email)
        response = self._Initialize_payment(amount,self.request.user.email)
        if response['status'] == True:
            # then the request was good we gonna take the person to paystack payment getway
            # so the user can pay
            "since the person has started the payment proccess let check if there is a batch that is open"
            raffle_batch ,created= models.RaffleDrawBatch.objects.get_or_create(is_close=False)
            "then we create a player ... and add that player to a BAtch"
            player = models.RaffleDrawPlayer.objects.create(
                    user = self.request.user,
                    raffle_draw_batch= raffle_batch,
                    isPayed = False,
                    amount = amount,
                    payment_reference =response['reference'])
            player.save()
            return HttpResponseRedirect(response['paystacklink'])
        else:
            # the person had some error then tak the person to the error page
            messages.success(self.request,response['message'])
            return redirect('errorpage')
        # return render(request,'raffleDraw/registerForGame.html')

    
    def _Initialize_payment(self,amount,email):
        # convert it to NGN
        amount = int(amount)
        url ='https://api.paystack.co/transaction/initialize'
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email":email, "amount":amount,
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
        

@csrf_exempt
def raffleDraw_callback(request):
    'THIS will just render the users a info page our webhook will handle the verfication of the payment'
    return render(request,'raffleDraw/paymentInfo.html')