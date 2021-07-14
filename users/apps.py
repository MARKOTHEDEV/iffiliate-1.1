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

    

        
        