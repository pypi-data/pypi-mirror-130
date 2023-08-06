from django.apps import AppConfig

from zweifach import checks


class ZweifachConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'zweifach'
