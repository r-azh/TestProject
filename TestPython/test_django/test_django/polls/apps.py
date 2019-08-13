from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'

    def ready(self):
        from . import signals
