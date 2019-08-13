from datetime import datetime
import json

import jsonpickle
__author__ = 'h.rouhani'


class Serializer:
    def add_handler(self, cls, handler):
        jsonpickle.handlers.registry.register(cls, handler)


    def serialize_to_string(self, data, include_class_path=True):
        if isinstance(data, str):
            return data

        # if isinstance(data, datetime):
        #     # datetime.isoformat()
        #     return data
        #
        # # jsonpickle.handlers.registry.register(datetime, DatetimeHandler)
        data_json_string = jsonpickle.encode(data, unpicklable=include_class_path)
        return data_json_string

    def serialize_to_dictionary(self, data, include_class_path=True):
        data_json_string = self.serialize_to_string(data, include_class_path)
        data_json_dictionary = json.loads(data_json_string)
        return data_json_dictionary



