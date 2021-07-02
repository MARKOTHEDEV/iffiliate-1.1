from django.test import TestCase
import requests,json
# Create your tests here.
PAYSTACK_SECRET_KEY   =  'sk_test_38a62cfc2939b3665f400a7c57bd61b7ab19f3fa'
PAYSTACK_PUBLIC_KEY  = 'pk_test_17925fc67c5b6da3dbef32feab9afccb0d175729'



def _Initialize_payment(amount,email):
    # convert it to NGN
    amount = int(amount)
    url ='https://api.paystack.co/transaction/initialize'
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
        "reason":"play betting game"
    }
    data = {
        "email":email, "amount":amount
    }
    response  = requests.post(url,data=json.dumps(data),headers=headers)

    try:
        response  = requests.post(url,data=json.dumps(data),headers=headers)
        responseData = response.json()
        print(responseData)
        if responseData['status'] == True and response.status_code == 200:
            
            return {'status':True,'message':responseData['message'],'link':responseData['data']['authorization_url']}
    except requests.exceptions.ConnectionError:
        return {'status':False,'message':'Network Problem'}
    


print(_Initialize_payment(1200,'ogechuwkumatthew@gmail.com'))