import datetime
from raffleDraw.models import RaffleDrawPlayer,RaffleDrawBatch
from django.contrib.auth import get_user_model
import random



def chooseRaffleDraw_winner_randomly():
    'get the current batch and randomly pick a winner'
    """
        So this is how it going to go 
        1) we going to get the batch that is not close and get all the players is related to it
        2) now all we have to do is  pick the player with the highest amount winner using the random module...
    """
    # check the Game if it open for players
    if  RaffleDrawBatch.objects.filter(is_close=False).exists() :
        currentBatch = RaffleDrawBatch.objects.get(is_close=False)

        allPlayers  = currentBatch.raffledrawplayer_set.all()
        # and check if the number of players is greater than 0 
        if len(allPlayers) > 0:
            # now let get the related players to the current batch
            # In this step we look for the hieghts amount
            highestAmount = max([player.amount  for player in allPlayers])
            # we fill the total amount paid in a batch
            currentBatch.totalAmountPaid_to_game +=sum([player.amount  for player in allPlayers])
            # we use that highestAmount to look up the winner
            Winner = currentBatch.raffledrawplayer_set.filter(amount=highestAmount)[0]
            # print(allPlayersMoney)e
            # randomWinner.user.userEarnings = 
            user = get_user_model().objects.get(email=Winner.user)
            # user.userEarnings =allPlayersMoney
            user.save()
            Winner.is_winner = True
            Winner.save()
            
            'we just close the batch That means the competiton is over'
            currentBatch.is_close = True
            currentBatch.save()

            # create another Batch(Like create another game)
            'since we start the game and end the game the same day '
            
            newGame,creadted= RaffleDrawBatch.objects.get_or_create(
                # since we close the previous batch on a sunday let add 5 more days so the game will start
                # the next comming sunday
                # we getting the for when and adding 5 more days to it
                is_close=False,
                when = currentBatch.when+datetime.timedelta(days=7)
            ) 
            newGame.save()
        else:
            'if we have no playerin the current batch create another batch just add 7 more days to the batch for the next Game'
            'we just close the batch That means the competiton is over'
            currentBatch.is_close = True
            currentBatch.save()
            newGame,creadted= RaffleDrawBatch.objects.get_or_create(
                # since we close the previous batch on a sunday let add 5 more days so the game will start
                # the next comming sunday
                # we getting the for when and adding 5 more days to it
                is_close=False,
                when = currentBatch.when+datetime.timedelta(days=7)
            ) 
            newGame.save()
            print('There Is no Player For this Game Yet')
    else:
        print("no co,mpetion yet")


