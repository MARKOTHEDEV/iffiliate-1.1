from django.contrib.auth.mixins import AccessMixin
from django.urls.base import reverse
from . import models 
import datetime,pytz
from django.shortcuts import redirect


def _format_django_date_to_pythondate(when_date):
    "this format to %y-%m-%d %I:%M:%S"
    currentWhen = datetime.datetime.strftime(when_date,'%y-%m-%d %I:%M:%S')
    parsed_currentWhen = datetime.datetime.strptime(currentWhen,'%y-%m-%d %I:%M:%S')

    return parsed_currentWhen
