__author__ = 'R.Azh'

#  install python-dateutil package
import dateutil.parser
import dateutil.relativedelta
import datetime

your_date = dateutil.parser.parse('2008-09-03T20:56:35.450686Z')     # RFC 3339 format
# gives : datetime.datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc())
print(your_date)

your_date = dateutil.parser.parse('2008-09-03T20:56:35.450686')  # ISO 8601 extended format
# gives : datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)
print(your_date)

your_date = dateutil.parser.parse('2008-09-03')  # ISO 8601 extended format
# gives : datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)
print(your_date)

your_date = dateutil.parser.parse('20080903T205635.450686')   # ISO 8601 basic format
# gives : datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)
print(your_date)

your_date = (dateutil.parser.parse('20080903')).date()   # ISO 8601 basic format, date only
# gives : datetime.datetime(2008, 9, 3, 0, 0)
print("date:", your_date)

print(datetime.datetime.utcnow().isoformat())

if dateutil.parser.parse("2008-3-1") < dateutil.parser.parse("2010-5-1"):
    print("hi")

dt = dateutil.parser.parse("Aug 28 1999 12:00AM")
print(dt)


def years_ago(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now()
    years_ago = from_date - dateutil.relativedelta.relativedelta(years=years)
    return years_ago

print(years_ago(10))  # gives date time of 10 years ago from now


def num_years(begin, end=None):
    if end is None:
        end = datetime.datetime.now()
    days = (end - begin).days
    if days > 0:
        num_years = int(days / 365.25)
    else:
        return 0
    if begin > years_ago(num_years, end):
        return num_years - 1
    else:
        return num_years

print(dt.year)
print(num_years(dt))  # number of years from dt to now

# implement years_age, months_ago, weeks_ago, days_ago

# dt = datetime.datetime.utcfromtimestamp(789264000000)
# print(dt)

date = dateutil.parser.parse('2016-10-03T00:00:00.000000')
date2 = date + datetime.timedelta(hours=23, minutes=59, seconds=59)
print(date)
print(date2)


value = abs((datetime.datetime.utcnow() - dateutil.parser.parse('2016-10-03T00:00:00.000000')).total_seconds()) < \
                                                2 * 7 * 24 * 3600
print(value)