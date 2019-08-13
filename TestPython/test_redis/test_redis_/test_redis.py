__author__ = 'R.Azh'

import redis


# create a connection to the localhost Redis server instance on port 6379
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# see what keys are in Redis
keys = redis_db.keys()
# output for keys() should be an empty list "[]"
print(keys)

out = redis_db.set(name='full stack', value='python')
print(out)

keys = redis_db.keys()
print(keys)

full_stack_value = redis_db.get('full stack')
print(full_stack_value)


# output is "1", we just incremented even though the key did not previously exist
int_val = redis_db.incr('int_val')
print(int_val)

# output is "b'1'" again, since we just obtained the value from the existing key
int_val = redis_db.get('int_val')
print(int_val)

out = redis_db.delete('int_val')
print(out)

int_val = redis_db.get('int_val')
print(int_val)
