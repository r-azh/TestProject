from datetime import datetime
import unittest
from bson import ObjectId
from pyutil.serialization.json.date_time_bson_serialize_handler import DatetimeBsonSerializeHandler
from pyutil.serialization.json.object_id_bson_serialize_handler import ObjectIdBsonSerializeHandler
from pyutil.serialization.json.serializer import Serializer

__author__ = 'R.Azh'


class TestSer(unittest.TestCase):
    def test_se(self):
        ser = Serializer()
        ser.add_handler(datetime, DatetimeBsonSerializeHandler)
        ser.add_handler(ObjectId, ObjectIdBsonSerializeHandler)
        res = ser.serialize_to_dictionary(
            [{'body': 'PERSON_EMAIL_EXIST', 'code': 'err2001', 'data': 'sysadmin@security.com'},
             {'body': 'PERSON_EMAIL_EXIST', 'code': 'err2001', 'data': 'sysadmin@security.com'}], False)

        print(res)
