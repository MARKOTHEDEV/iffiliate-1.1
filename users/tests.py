from django.test import TestCase

# Create your tests here.


import datetime,time

# time.strftime()


# datetime.datetime.now(),
today = datetime.datetime.strftime(datetime.datetime.now(),'%y-%m-%d')
parsed = datetime.datetime.strptime(today,'%y-%m-%d')
