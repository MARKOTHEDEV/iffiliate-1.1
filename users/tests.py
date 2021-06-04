'''
    Steps for user payment

    check if it 30th then show button to make transfer
    onclick of the transfer button it takes os to a page were user Can
            input thier bank account
            select bank Name -> genarated by jinja template

            on click of submit button

            we use the select back to get the bank code

'''


{'status': True, 
'message': 'Transfer recipient created successfully',

'data': {'active': True, 'createdAt': '2021-05-17T19:28:26.000Z',
'currency': 'NGN', 'description': None, 'domain': 'test', 'email': None,
'id': 14385883, 'integration': 579669, 'metadata': None,
'name': 'OGECHUKWU MATTHEW NWOKOLO', 'recipient_code': 'RCP_b5brnbx0fz516w4',
'type': 'nuban', 'updatedAt': '2021-05-17T19:28:26.000Z', 'is_deleted': False,
     'details': {'authorization_code': None, 'account_number': 
     '2209134092', 'account_name': 'OGECHUKWU MATTHEW NWOKOLO', 
     'bank_code': '057', 'bank_name': 'Zenith Bank'}
     }}

import requests,json

PAYSTACK_SECRET_KEY   =  'sk_test_38a62cfc2939b3665f400a7c57bd61b7ab19f3fa'

# url https://api.paystack.co/transfer

# -H "Authorization: Bearer YOUR_SECRET_KEY"

# -H "Content-Type: application/json"

# -d '{ "source": "balance", 

#       "amount": "3794800", 

#       "recipient": "RCP_t0ya41mp35flk40", 

#       "reason": "Holiday Flexing" 

#     }'
url = 'https://api.paystack.co/transfer'
header = {
     "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
     "content-Type": "application/json",
      'Accept': 'application/json',
}
data = {
     "source": "balance","amount": "39800","recipient": "RCP_b5brnbx0fz516w4",
     "reason": "Holiday Flexing" ,
     'redirect_url' :'/user/'
}
data =json.dumps(data)

resp = requests.post(url=url,data=data,headers=header)
print(resp.json())


# 2209134092