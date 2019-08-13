from django.db.models.signals import post_save
from django.dispatch import receiver
from TestPython.test_django.test_django.polls.models import Question
from django.core.cache import cache
__author__ = 'R.Azh'

# The Django Signals is a strategy to allow decoupled applications to get notified when certain events occur.


@receiver(post_save, sender=Question)
def put_last_result_in_cache(sender, instance, created, **kwargs):
    # do something
    cache.set('key', 'value', 2*60)
    print(cache.get('key'))
    print(sender)
    print(instance)
    # print(instance.something.pk)
    from django.utils import timezone

    print(timezone.now())