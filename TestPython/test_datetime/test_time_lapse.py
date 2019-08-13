__author__ = 'R.Azh'


from datetime import datetime

import time


# import datetime
import bson
from bson.objectid import ObjectId

b = ObjectId()
dt = b.generation_time
print(type(dt))

ts1 = datetime.now().timestamp()

time.sleep(1)

ts2 = datetime.now().timestamp()

print(ts2 - ts1)


# time_delta = datetime.now(timezone.utc) - ObjectId(self.comment_id).generation_time.replace(tzinfo=timezone.utc)
# if time_delta < timedelta(minutes=5):