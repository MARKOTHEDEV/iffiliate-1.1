from django.test import TestCase
import requests,json
# Create your tests here.
{'event': 'charge.success',
 'data': {'id': 1204292261, 'domain': 'test', 'status': 'success', 'reference': 'liym5r51vf'
 , 'amount': 1000, 'message': None, 'gateway_response': 'Successful', 'paid_at': '2021-07-05T12:35:35.000Z',
  'created_at': '2021-07-05T12:35:25.000Z', 'channel': 'card', 'currency': 'NGN', 'ip_address': '197.210.70.26', 
  'metadata': {'custom_fields': {'paymentFor': 'raffle_game'}}, 'log': {'start_time': 1625420109, 'time_spent': 9,
   'attempts': 1, 'errors': 0, 'success': True, 'mobile': False, 'input': [],
   
'history': [{'type': 'action', 'message': 'Attempted to pay with card','time':  3},
{'type': 'success', 'message': 'Successfully paid with card', 'time': 9}]},
'fees': 15, 'fees_split': None, 'authorization': 
{'authorization_code': 'AUTH_t85sbj3yif', 'bin': '408408', 'last4': '4081', 'exp_month': '12',
 'exp_year': '2030', 'channel': 'card', 'card_type': 'visa ', 'bank': 'TEST BANK',
  'country_code': 'NG', 'brand': 'visa', 'reusable': True, 'signature': 'SIG_MnlBma3Ma6Cag9dTk0yj', 
  'account_name': None, 'receiver_bank_account_number': None, 'receiver_bank': None}, 
  'customer': {'id': 39766703, 'first_name': None, 'last_name': None, 'email': 'marko@gmail.com', 
  'customer_code': 'CUS_jnrm3x1t5xvwlvi', 'phone': None, 'metadata': None, 'risk_action': 'default',
   'international_format_phone': None}, 'plan': {}, 'subaccount': {}, 'split': {}, 'order_id': None,
    'paidAt': '2021-07-05T12:35:35.000Z', 'requested_amount': 1000, 'pos_transaction_data': None, 
    'source': {'type': 'api', 'source': 'merchant_api', 'identifier': None}}, 'order': None, 
'business_name': 'MARKOTHEDEV'}


amount = 500


amount = float(amount)*100
print(amount,'float')
amount = int(amount)
print(amount,'int')


def c(kobo):
    kobo = float(kobo)/100
    kobo = int(kobo)
    return kobo


print(c(amount))