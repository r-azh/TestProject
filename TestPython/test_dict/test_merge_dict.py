from copy import deepcopy
from pprint import pprint

default_data = {
  "notifications": {
    "update": {
      "outlets": {
        "sms": {
          "status": "active",
          "frequency": ""
        },
        "email": {
          "status": "active",
          "frequency": ""
        },
        "slack": {
          "status": "active",
          "frequency": ""
        },
        "telegram": {
          "status": "active",
          "frequency": ""
        },
        "push": {
          "status": "active",
          "frequency": ""
        }
      }
    }
  }
}

new_data = {
    "notifications": {
        "update": {
            "outlets": {
                "sms": {
                    "status": "inactive",
                    "frequency": "5"
                },
            "push": {
                "status": "inactive",
                "frequency": "40"
            }
            }
        }
    }
}


def merge_dicts(default, new_data):
    for key, value in new_data.items():
        if isinstance(value, dict):
            merge_dicts(default[key], new_data[key])
        else:
            default[key] = new_data[key]


def merge_dicts_with_return(default, new_data):
    data = deepcopy(default)
    for key, value in new_data.items():
        if isinstance(value, dict):
            data[key] = merge_dicts_with_return(data[key], new_data[key])
        else:
            data[key] = new_data[key]
    return data


merge_dicts(default_data, new_data)

pprint(default_data)


result = merge_dicts_with_return(default_data, new_data)

pprint(result)