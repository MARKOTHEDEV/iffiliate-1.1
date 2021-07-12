from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.db.utils import OperationalError

        try:
            # self._create_defualt_model_instance()
            from users import signals
            from users.cronjobs import cronjob
            
            cronjob.start()
        except OperationalError:
            pass

    

    def _create_defualt_model_instance(self):
        'this function create models that are very important! to run the app without them the app will fail!'
        from . import models
        freeMembership,created = models.Membership.objects.get_or_create(slug='Free')
        freeMembership.save()
        
        