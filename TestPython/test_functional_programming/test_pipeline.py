from functools import reduce

__author__ = 'R.Azh'

print('\n############### imperative #######################')

bands = [{'name': 'sunset rubdown', 'country': 'UK', 'active': False},
         {'name': 'women', 'country': 'Germany', 'active': False},
         {'name': 'a silver mt. zion', 'country': 'Spain', 'active': True}]


def format_bands(bands):
    for band in bands:
        band['country'] = 'Canada'
        band['name'] = band['name'].replace('.', '')
        band['name'] = band['name'].title()

format_bands(bands)

print(bands)

#  It is hard to tell what the code is intended to do and hard to tell if it does what it appears to do.
# The code is hard to reuse, hard to test and hard to parallelize.

print('\n############### functional #######################')


def assoc(_d, key, value):
    from copy import deepcopy  # produce a copy of the passed dictionary.
    d = deepcopy(_d)
    d[key] = value
    return d


def set_canada_as_country(band):
    return assoc(band, 'country', "Canada")


def strip_punctuation_from_name(band):
    return assoc(band, 'name', band['name'].replace('.', ''))


def capitalize_names(band):
    return assoc(band, 'name', band['name'].title())

# Band dictionary originals are protected from mutation when a key is associated with a new value.
#  But there are two other potential mutations in the code above.
# If replace() and title() are not functional, strip_punctuation_from_name() and capitalize_names() are not functional.
# Fortunately, replace() and title() do not mutate the strings they operate on. This is because strings
# are immutable in Python.


def pipeline_each(data, fns):
    return reduce(lambda a, x: map(x, a),
                  fns,
                  data)

print(list(pipeline_each(bands, [set_canada_as_country,
                                 strip_punctuation_from_name,
                                 capitalize_names])))

print('\n############### functional: even better #######################')


def call(fn, key):
    def apply_fn(record):
        return assoc(record, key, fn(record.get(key)))
    return apply_fn


set_canada_as_country = call(lambda x: 'Canada', 'country')
strip_punctuation_from_name = call(lambda x: x.replace('.', ''), 'name')
capitalize_names = call(str.title, 'name')

print(list(pipeline_each(bands, [set_canada_as_country,
                                 strip_punctuation_from_name,
                                 capitalize_names])))

# call() could be used to generate pipeline functions for any program, regardless of topic.
# Functional programming is partly about building up a library of generic, reusable, composable functions.


print('\n############### not functional #########################')


def extract_name_and_country(band):
    plucked_band = {}
    plucked_band['name'] = band['name']
    plucked_band['country'] = band['country']
    return plucked_band

print(list(pipeline_each(bands, [call(lambda x: 'Canada', 'country'),
                         call(lambda x: x.replace('.', ''), 'name'),
                         call(str.title, 'name'),
                         extract_name_and_country])))

print('\n###############  functional #########################')


def pluck(keys):
    def pluck_fn(record):
        return reduce(lambda a, x: assoc(a, x, record[x]),
                      keys,
                      {})
    return pluck_fn

print(list(pipeline_each(bands, [call(lambda x: 'Canada', 'country'),
                         call(lambda x: x.replace('.', ''), 'name'),
                         call(str.title, 'name'),
                         pluck(['name', 'country'])])))