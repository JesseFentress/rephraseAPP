from django.apps import AppConfig


class RephraseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rephrase'

    def ready(self):
        from .import signals