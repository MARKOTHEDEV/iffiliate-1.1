
from django.apps import AppConfig


class RaffledrawConfig(AppConfig):
    name = 'raffleDraw'

    def ready(self):
        from django.db.utils import OperationalError
        try:

            # self._create_defualt_model_instance()
            2*2
        except OperationalError:
            pass


    def _create_defualt_model_instance(self):
        'this function create models that are very important! to run the app without them the app will fail!'
        from . import models

        createRaffeBatch,created= models.RaffleDrawBatch.objects.get_or_create(is_close=False)
        createRaffeBatch.save()