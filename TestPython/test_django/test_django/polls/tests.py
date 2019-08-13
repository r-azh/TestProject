from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
import pickle
from .models import Question


class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_pickling_cache_object(self):
        p = pickle.dumps(self.cache)
        cache = pickle.loads(p)
        # Now let's do a simple operation using the unpickled cache object
        cache.add("addkey1", "value")
        result = cache.add("addkey1", "newvalue")
        self.assertEqual(result, False)
        self.assertEqual(cache.get("addkey1"), "value")

    def test_djanog_cache(self):
        from django.core.cache import cache
        cache.set("rezvan_key", "rezvan_value")
        cache_value = cache.get("rezvan_key")
        self.assertEqual(cache_value, "rezvan_value")

# sudo python3.4  manage.py test