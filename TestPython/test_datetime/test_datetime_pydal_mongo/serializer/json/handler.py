import calendar
import jsonpickle
from jsonpickle.handlers import BaseHandler

__author__ = 'H.Rouhani'


class DatetimeHandler(BaseHandler):
    def flatten(self, obj, data):
        return obj.isoformat()

    # def flatten(self, obj, data):
    #     res = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
    #     return {"$date": res}

    def restore(self, obj):
        return obj


class ObjectIdBsonSerializeHandler(BaseHandler):
    def flatten(self, obj, data):
        return {"$oid": str(obj)}

    def restore(self, data):
        return data