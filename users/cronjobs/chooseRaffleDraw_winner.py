from raffleDraw.models import RaffleDrawPlayer,RaffleDrawBatch
import random



def chooseRaffleDraw_winner_randomly():
    'get the current batch and randomly pick a winner'
    """
        So this is how it going to go 
        1) we going to get the batch that is not close and get all the players is related to it
        2) now all we have to do is randomly pick the winner using the random module...
    """

    if  RaffleDrawBatch.objects.filter(is_close=False).exists():
        currentBatch = RaffleDrawBatch.objects.get(is_close=False)
        # now let get the related players
        allPlayers  = currentBatch.raffledrawplayer_set.all()
        randomWinner = random.choice(allPlayers)
        randomWinner.is_winner = True
        randomWinner.save()
        'we just close the batch That means the competiton is over'
        currentBatch.is_close = True
        currentBatch.save()
    else:
        print("no co,mpetion yet")


