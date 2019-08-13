import jsonpickle
from datetime import datetime
import jsonpickle.handlers

time = jsonpickle.encode(datetime.now(), unpicklable=False)

print(time)


########## produce ISO 8601 format ################

class DatetimeHandler(jsonpickle.handlers.BaseHandler):
    def flatten(self, obj, data):
        return obj.isoformat()

jsonpickle.handlers.registry.register(datetime, DatetimeHandler)
time = jsonpickle.encode(datetime.now(), unpicklable=False)
print(time)
