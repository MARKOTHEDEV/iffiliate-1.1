import requests,json
from pathlib import Path
from django.conf import settings

import os

PAYSTACK_SECRET_KEY   =  'sk_test_38a62cfc2939b3665f400a7c57bd61b7ab19f3fa'






class UserPaymentPreparation:


    def __init__(self):
        'allow us to set the amout any time'
        self.amount =0



    """
    this class handles every thing to prepare the user for payment
    it doesnt pay the user it runs fo verication it pass it goes saves the user in the database
    allowing the user to be ready for payment
    it the user Payment class that pays the user
    IT THE ADMIN that will triger the userPayment class
    """


    def get_bankCodeFromJSON(self):
        'this function avoid repeating calling the json file'
        with open('./users/bankCode.json','r') as bankCodes:
            return json.loads(bankCodes.read())
   
    def get_available_bank_name(self):
        """
            this method returns a list of available bank names
            javascript will manipulate in such a way that the user will click it 

        """
        allBankCode = self.get_bankCodeFromJSON()
        list_of_bank_names = []
        for bank in allBankCode:
            list_of_bank_names.append(bank.get('name'))

        return list_of_bank_names

    def get_bank_code(self,bankName):

        """
            this method takes in a second parameter called bankName
            js will send a Bank name the user click now we will write a if statment to get the bank code
            THIS WILL RETURN A DICTIONARY THAT CONTAINS THE SPECIFIC BANK CODE  
        """
        
        
        allBankCode = self.get_bankCodeFromJSON()
        
        for bank in allBankCode:
            # list_of_bank_names.append(bank.get('name'))
            if bankName == bank.get('name'):
            
                correctBank = bank
                
                # print(bankName,bank.get('name'))
        return correctBank

    def create_transfer_recipient(self,data):
        url = f'https://api.paystack.co/transferrecipient'
        headers = {
            'Authorization': 'Bearer '+PAYSTACK_SECRET_KEY,
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
        }
        try:
            resp = requests.post(url,headers=headers,data=json.dumps(data))
            
            return resp.json()
        except requests.exceptions.ConnectionError:
            return {'status':False,'message':'Network Problem'}



    def test_user_account(self,accountNumber,bankCode,Bankname):
        'this test the user account if it valid or not'
        'if yes we save the data to a database'
        # print(accountNumber,bankCode)
        
        url = f'https://api.paystack.co/bank/resolve?account_number={accountNumber}&bank_code={bankCode}'
        headers = {
            'Authorization': 'Bearer '+PAYSTACK_SECRET_KEY,
            'Content-Type' : 'application/json',
            'Accept': 'application/json',


        }
        try:
            resp = requests.get(url,headers=headers)
            respData = resp.json()


            if respData.get('status') == True:
                # if the user test account passed then we need to create a transfer recipient
                # after we save the recipient,amount to database then the user is ready for payment
                DATA = { "type": Bankname,"name": respData.get('data').get('account_name'),
                "account_number": respData.get('data').get('account_number'),
                "bank_code": bankCode, "currency": "NGN"}

                return self.create_transfer_recipient(DATA)
            
            else:

                return respData

        except requests.exceptions.ConnectionError:
            return {'status':False,'message':'Network Problem'}

    def run(self,bankName,realAcctNum):
        
        bankInfo = userpayHandler.get_bank_code(bankName)
        PaystackInfo = userpayHandler.test_user_account(realAcctNum,bankInfo.get('code'),bankName)

        return PaystackInfo

        

"""
    UserPaymentPreparation aclass that prepares user for payment more like filter the unQualified ones
    STEPS 
    We need toc check if the use is enabled for payment if yes
    all we need is the user account number and bank name
        to show the user availble bank name we use UserPaymentPreparation.get_available_bank_name() it returns all the bank name
        we can use js to manipulate it for the user to pick the bank

        after we call the UserPaymentPreparation.test_user_account() we check if status is true or false
        if true we save data to this model

        UserRequestPayment MOdel:
                is going to contain 
                username foregin key with the logged in user
                amount -- 
                ispaid -- boolean field
                isreadyForPayment -- boolean field
                account_number -- the user account number 
                account_name -- the user account number 
                bank_code
                bank_name
                recipient_code = will save this when i make a request to https://api.paystack.co/transferrecipient

"""


userpayHandler = UserPaymentPreparation()
# so we will use this in the view to render the list of avilable banks
name = userpayHandler.get_available_bank_name()
# this will return status true of false we work with that from there
# if the bool is True we save it in our     UserRequestPayment
print(userpayHandler.run('Zenith Bank',realAcctNum))



# 'in this test i will be using my Zenith Bank account'
# bankInfo = userpayHandler.get_bank_code('Zenith Bank')
# # realAcctNum +='33342'
# PaystackInfo = userpayHandler.test_user_account(realAcctNum,bankInfo.get('code'),'Zenith Bank')
# # this willl be a dictionary that will have a key called status
# # if status is true safe to UserRequestPayment database
# # else status is false send use the ['message'] which will have message ont the failure


# if PaystackInfo.get('status') == True:
#     # this happens if it passed
#     # next step 
#         # @erase the userPaymnet
#         # create a new intance of UserRequestPayment fill it with data gotten from paystack
        
#     print(PaystackInfo)

# else:
#     # this happens if it failed
#     print(PaystackInfo)




