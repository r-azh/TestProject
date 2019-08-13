# https://sendy.co/api
# sendy installation url
# fixme
import json

import requests

url = "http://mail.pouyarasaneh.com/sendy"


subscribe_link = f"{url}/subscribe"
unsubscribe_link = f"{url}/unsubscribe"

# user info
id_list = ['7KHbys9MYTIuoEFk0QmZkQ']
# id_list = [1]
dto = {
    "email": "test@test.com",
    "boolean": 'true',
    "list": id_list

}
optional_fields = {
    "name": "test",
    "country": "US",
    "ipaddress": "127.0.0.1",
    "referrer": "test.com",
    "gdpr": False,
    "hp": "",
}

# response = requests.post(subscribe_link, json=dto)
# headers = {'Content-type': 'application/x-www-form-urlencoded'}
# response = requests.post(subscribe_link, data=json.dumps(dto), headers=headers)
# subscribe
response = requests.post(subscribe_link, data=dto)
print(response.text)
assert response.text == '1'

# unsubscribe
response = requests.post(unsubscribe_link, data=dto)
print(response.text)
assert response.text == '1'