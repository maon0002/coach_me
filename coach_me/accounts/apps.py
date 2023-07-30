from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coach_me.accounts'

    def ready(self):
        import coach_me.accounts.signals
        result = super().ready()
        # from .signals import *

        return result
