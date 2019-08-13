from urllib import parse

some_random_string = 'aseuoiur79869323./sdjfld\dsdfjdf:"Jed'
print(some_random_string)

quote_plus = parse.quote_plus(some_random_string)
print(quote_plus)
unquote = parse.unquote(quote_plus)
print(unquote)
assert some_random_string == unquote


f = {'eventName': 'myEvent', 'eventDescription': 'cool event'}
print(parse.urlencode(f))


def _prepare_for_url(string):
    control_characters = [u'\u001F', u'\u007F']
    space_characters = [u'\u0020']
    delimiter_characters = ["<", ">", "#", "%", '"']
    unwise_characters = ["{", "}", "|", "\\", "^", "[", "]", "`"]
    reserved_characters = [";", "/", "?", ":", "@", "&", "=", "+", "$", ",", "."]
    for item in control_characters + space_characters + delimiter_characters + unwise_characters \
                + reserved_characters:
        string = string.replace(item, '')
    return string

print(_prepare_for_url(some_random_string))