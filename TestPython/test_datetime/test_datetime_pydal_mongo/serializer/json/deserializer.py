import json

import jsonpickle

__author__ = 'h.rouhani'


class Deserializer:
    def deserialize_from_string(self, json_string):
        data = jsonpickle.decode(json_string)
        return data

    def deserialize_from_dictionary(self, json_dictionary):
        data_json_string = json.dumps(json_dictionary)
        return self.deserialize_from_string(data_json_string)
