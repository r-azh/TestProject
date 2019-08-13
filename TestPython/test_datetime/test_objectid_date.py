from datetime import datetime, timezone, timedelta
from time import sleep
from bson import ObjectId

__author__ = 'R.Azh'

id = ObjectId()
print(id)

print(id.generation_time)

sleep(3)
id2 = ObjectId()
print(id2.generation_time)

print(id.generation_time.utcoffset())

# naive_date_time = id.generation_time.replace(tzinfo=None)
# delta = datetime.utcnow() - naive_date_time

# delta = datetime.now(timezone.utc) - id.generation_time

# delta = datetime.now() - id.generation_time.replace(tzinfo=None)
delta = datetime.now(timezone.utc) - id.generation_time.replace(tzinfo=timezone.utc)

print('delta :', delta)

if delta < timedelta(seconds=3):
    print('under 3 ')
else:
    print('over 3')


id3 = ObjectId('57ca7b1f3ae7282cec35fb93')
print(id3)