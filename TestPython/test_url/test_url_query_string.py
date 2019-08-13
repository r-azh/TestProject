__author__ = 'R.Azh'

try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

url = "http://stackoverflow.com/search?q=question"
url = "http://amir.parsadp.com/api/v1.0/persons/advanced_search?skip=0&operator=and&sort=name%2Clast_name&criteria" \
      "=experience_company_name%3Agoogle%2Cexperience_title%3Aexperience&take=150"
params = {'lang': 'en', 'tag': 'python'}

url_parts = list(urlparse.urlparse(url))
print(url_parts)
query = dict(urlparse.parse_qsl(url_parts[4]))
print(query)
query.update(params)
print(query)

url_parts[4] = urlencode(query)

print(urlparse.urlunparse(url_parts))
