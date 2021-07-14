from django.contrib.auth.mixins import AccessMixin
from django.urls.base import reverse
from . import models 
import datetime,pytz
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages


def _format_django_date_to_pythondate(when_date):
    "this format to %y-%m-%d %I:%M:%S"
    currentWhen = datetime.datetime.strftime(when_date,'%y-%m-%d %I:%M:%S')
    parsed_currentWhen = datetime.datetime.strptime(currentWhen,'%y-%m-%d %I:%M:%S')

    return parsed_currentWhen


class CheckGame(AccessMixin):
    'this class is based off access mixin it checks if a game is online or not'
    login_required_message = 'You have To login To Play the Game!!'
    login_url = 'signin'
    
    # this is the RaffleDrawBatch
    model = models.RaffleDrawBatch
    def check_game_is_open(self):
        if self.model.objects.filter(is_close=False).exists():
            'we search if there is a Open Game'
            return True
        else:
            'This means There Is no Game At the Moment'
            return False


    

    def dispatch(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        print(self.login_url)
        if request.user.is_authenticated == False:
            'This just makes Sure the user Is logged In'
            messages.error(request,self.login_required_message)
            return redirect(self.login_url)

        else:
            if not self.check_game_is_open():
                'if it not true Take the person'
                return redirect('gameNotAvaliable')
        return super(CheckGame, self).dispatch(request, *args, **kwargs)
    

