from urllib.parse import urlencode, quote_plus

__author__ = 'R.Azh'


# urllib.parse.urlencode(query[, doseq])
param_str = "vvpGWKNtQ0G82X9BBZJc4w+ahRAFxeLDkG9t3HtoczKq/a9ezrFhmx3CGAVQ4quH6cSHkYPY3URFWq1qdvg17i" \
    "\ihJerXYocc3XK8h2lUOSmRaaZHKOS5zOKTTku4duP".encode('utf-8')

url_str = 'http://tamir.parsadp.com/user_accounts/password_reset?vvpGWKNtQ0G82X9BBZJc4w+ahRAFxeLDkG9t3HtoczKq/a9ezrFhmx3CGAVQ4quH6cSHkYPY3URFWq1qdvg17i/ihJerXYocc3XK8h2lUOSmRaaZHKOS5zOKTTku4duP'

# encoded_url = urlencode(url_str)
encoded_url = quote_plus(url_str)
encoded_param = quote_plus(param_str)
encoded_param.encode('utf-8')
print(param_str)
print(encoded_param)
print(encoded_url)
