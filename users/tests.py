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


a = {'s':1}

a.update({'1':'3'})
print(a)