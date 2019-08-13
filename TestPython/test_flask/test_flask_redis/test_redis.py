from TestPython.test_flask.test_flask_redis import redis_store

result = redis_store.get('potato')
print(result)

redis_store.set('potato', 'potato')
result = redis_store.get('potato')
print(result)