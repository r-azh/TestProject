import threading
from time import sleep
from unittest import TestCase
import datetime

from sqlalchemy import text

from interactive_secure_links.python.hash.hash_implementation_sample.app import app, db
from interactive_secure_links.python.hash.hash_implementation_sample.hash_implementation import create_hash_log, \
    create_hash, get_hash_from_link_hash, get_hash_from_cash, init_hash_cache
from interactive_secure_links.python.hash.hash_implementation_sample.models import User, InteractiveSecureLinkHash, \
    InteractiveSecureLinkHashAccessLog


def insert_test_users():
    user1 = User.query.filter(User.email == 'john@pouya.com').first()
    user2 = User.query.filter(User.email == 'jane@pouya.com').first()
    if user1 is None:
        user1 = User('john', 'Doe', 'john@pouya.com', '123')
        db.session.add(user1)
    if user2 is None:
        user2 = User('jane', 'Doe', 'jane@pouya.com', '123')
        db.session.add(user2)
    db.session.commit()
    return user1.id, user2.id


def bulk_insert_into_hash_table(user_id, limit):
    query_txt = text(
        f"insert into interactive_secure_link_hashes(hash, expiry_ts, usage_limit, user_id, module_id) "
        f"select md5(i::text), '{datetime.datetime.utcnow() + datetime.timedelta(days=100)}'::date, "
        f"5, {user_id}, 'module_1' "
        f"from generate_series(1, {limit}) s(i); ")
    db.engine.execute(query_txt)


class AccessHash(threading.Thread):
    def __init__(self, threadID, hash, limit):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.hash = hash
        self.counter = 0
        self.limit = limit
        self._stop_event = threading.Event()

    def run(self):
        while self.limit:
            if self._stop_event.is_set():
                break
            else:
                create_hash_log(self.hash)
                self.limit -= 1
                self.counter += 1

    def stop(self):
        self._stop_event.set()


class TestHash(TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

        self.user_id1, self.user_id2 = insert_test_users()
        count = InteractiveSecureLinkHash.query.count()
        if count == 0:
            bulk_insert_into_hash_table(self.user_id1, 1000000)

    # or
    # def create_app(self):
    #     app.config['TESTING'] = True
    #     app.app_context().push()
    #     db.create_all()
    #     return app

    # todo reasonable access time --> cache
    def test_hash_table_should_have_reasonable_access_time(self):

        hash1 = InteractiveSecureLinkHash.query.order_by(InteractiveSecureLinkHash.hash.desc()).first()

        start = datetime.datetime.utcnow()
        finded_hash = InteractiveSecureLinkHash.query.get(hash1.hash)
        elapsed = datetime.datetime.utcnow() - start
        assert finded_hash is not None
        assert elapsed < datetime.timedelta(milliseconds=100)

    # todo test cache
    def test_retrieve_hash_should_have_reasonable_access_time(self):
        init_hash_cache()
        hash1 = InteractiveSecureLinkHash.query.order_by(InteractiveSecureLinkHash.hash.desc()).first()

        start = datetime.datetime.utcnow()
        cached_hash = get_hash_from_cash(hash1.hash)
        elapsed = datetime.datetime.utcnow() - start
        assert cached_hash is not None
        assert elapsed < datetime.timedelta(milliseconds=100)


    # todo always correct access log
    def test_hash_access_log_should_store_a_log_for_every_access(self):
        InteractiveSecureLinkHashAccessLog.query.delete()
        _, hash1 = create_hash(self.user_id1)
        _, hash2 = create_hash(self.user_id2)

        access_hash_thread_1 = AccessHash('access_hash_1', hash1.hash, 100000)
        access_hash_thread_2 = AccessHash('access_hash_2', hash1.hash, 100000)
        access_hash_thread_3 = AccessHash('access_hash_3', hash1.hash, 100000)
        access_hash_thread_4 = AccessHash('access_hash_4', hash2.hash, 100000)
        access_hash_thread_5 = AccessHash('access_hash_5', hash2.hash, 100000)

        access_hash_thread_1.start()
        access_hash_thread_2.start()
        access_hash_thread_3.start()
        access_hash_thread_4.start()
        access_hash_thread_5.start()
        sleep(30)
        access_hash_thread_1.stop()
        access_hash_thread_2.stop()
        access_hash_thread_3.stop()
        access_hash_thread_4.stop()
        access_hash_thread_5.stop()

        access_count = access_hash_thread_1.counter + access_hash_thread_2.counter + access_hash_thread_3.counter \
                       + access_hash_thread_4.counter + access_hash_thread_5.counter
        stored_logs_count = InteractiveSecureLinkHashAccessLog.query.count()
        assert stored_logs_count == access_count
    #     fixme

    # todo always correct usage_count
    def test_hash_total_access_should_have_correct_value_all_the_time(self):
        pass

    def test_gc_should_be_able_to_remove_all_hash_based_on_user(self):
        start = datetime.datetime.utcnow()

        User.query.filter(User.id == self.user_id1).delete()
        elapsed = datetime.datetime.utcnow() - start
        assert elapsed < datetime.timedelta(seconds=30)

        count = InteractiveSecureLinkHash.query.count()
        assert count == 0

    def test_gc_should_be_able_to_remove_all_hash_based_on_expiry_ts(self):
        start = datetime.datetime.utcnow()

        InteractiveSecureLinkHash.query\
            .filter(InteractiveSecureLinkHash.expiry_ts <= datetime.datetime.utcnow() + datetime.timedelta(days=101))\
            .delete()
        elapsed = datetime.datetime.utcnow() - start
        assert elapsed < datetime.timedelta(seconds=30)

        count = InteractiveSecureLinkHash.query.count()
        assert count == 0

    def test_hash_store_in_db_should_be_equal_to_hashed_hash_from_link_with_salt(self):
        hash_str, _ = create_hash(self.user_id1)
        retrieved_hash = get_hash_from_link_hash(hash_str)
        stored_hash = InteractiveSecureLinkHash.query.filter(InteractiveSecureLinkHash.hash == retrieved_hash.decode()).all()
        assert len(stored_hash) == 1

