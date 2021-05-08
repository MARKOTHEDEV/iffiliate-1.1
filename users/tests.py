import requests,json
from pathlib import Path



PAYSTACK_SECRET_KEY   =  'sk_test_38a62cfc2939b3665f400a7c57bd61b7ab19f3fa'
PAYSTACK_PUBLIC_KEY  = 'pk_test_17925fc67c5b6da3dbef32feab9afccb0d175729'






# url = 'https://api.paystack.co/transaction/initialize'
# 'so now we just arangig requests parameter '
# 'the request must have a valid email and price'
# headers = {
    # 'Authorization': 'Bearer '+PAYSTACK_SECRET_KEY,
    # 'Content-Type' : 'application/json',
    # 'Accept': 'application/json',
    

#     }
# body = {
#     "email": request.user.email,
#     "amount": price
#     }

realAcctNum ='2209134092'

# x = requests.post(url, data=json.dumps(body), headers=headers)


# userInput = input('enter bank name:')

# with open('./users/bankCode.json','r') as bankCodes:
#     allBankCode = json.loads(bankCodes.read())

#     for bank in allBankCode:
#         print(bank.get('name'))


class UserPaymentPreparation:
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


    def test_user_account(self,accountNumber,bankCode):
        'this test the user account if it valid or not'
        'if yes we save the data to a database'
        print(accountNumber,bankCode)
        
        url = f'https://api.paystack.co/bank/resolve?account_number={accountNumber}&bank_code={bankCode}'
        headers = {
            'Authorization': 'Bearer '+PAYSTACK_SECRET_KEY,
            'Content-Type' : 'application/json',
            'Accept': 'application/json',


        }
        resp = requests.get(url,headers=headers)

        print(resp.json())


userpayHandler = UserPaymentPreparation()


name = userpayHandler.get_available_bank_name()

'in this test i will be using my Zenith Bank account'
bankInfo = userpayHandler.get_bank_code('Zenith Bank')
realAcctNum +='33342'
IsUserAcountValid = userpayHandler.test_user_account(realAcctNum,bankInfo.get('code'))

