from django.db import models
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError


# Create your models here.

class RaffleDrawBatch(models.Model):
    'this model will help me group the candidate into groups'
    totalAmountPaid_to_game = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ,blank =True) 
    # if is_close is True then nobody can apply to that batch--meaning we have already seen the winner of the batch
    is_close = models.BooleanField(default=False)
    # this is created when an instance is created u cant modify it!!
    created_on = models.DateTimeField(auto_now_add=True)
    # when = models.DateTimeField(null=True)


    def __str__(self):
        return f'Batch {self.id}'

class RaffleDrawPlayer(models.Model):
    'this is modeling a player that will play the raffle draw'
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    raffle_draw_batch = models.ForeignKey(RaffleDrawBatch,on_delete=models.CASCADE,null=True)
    isPayed = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ,blank =True)
    payment_reference = models.CharField(max_length=30,blank=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

