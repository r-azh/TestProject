import locale
from dateutil.tz import tzutc
from datetime import datetime, timezone, timedelta
__author__ = 'R.Azh'

print("\niso time :")
#   time adjusted for current timezone # Local to ISO-8601 : example: 2010-12-16 17:22:15 or 20101216T172215
date_now = datetime.now().isoformat()
print(date_now)

#   unadjusted UTC time # UTC to ISO-8601
date_utc_now = datetime.utcnow().isoformat()
print(date_utc_now)

my_date = datetime(2002, 12, 4, 12, 30).isoformat()
print(my_date)

parsed_date = datetime.strptime(my_date, "%Y-%m-%dT%H:%M:%S" )
print(parsed_date)

print("\nsubtract time - not iso :")
#  subtract time
date_now = datetime.now()
print(date_now)
date_utc_now = datetime.utcnow()
print(date_utc_now)

delta = date_now - date_utc_now
if delta > timedelta(0, 0, 0, 0, 0, 0, 0):
    print(delta)   # timedelta type

print("\naware time : ")
#   timezone aware UTC
my_date = datetime.now(timezone.utc).isoformat()
print(my_date)

#   get local time : tehran UTC+3:30
my_date = datetime.now(timezone.utc).astimezone().isoformat()
print(my_date)


print("\ntime samples: ")
print(datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc()))
print(datetime(2008, 9, 3, 20, 56, 35, 450686))
print(datetime(2008, 9, 3, 0, 0))

#   parse string to time, but dateutil is easier
date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
print(date_object)

my_date = datetime(2002, 12, 4, 12, 30)
if my_date < datetime.utcnow():
    print("less")

my_date = None
mydate2 = my_date or None
print( "mydate2:", mydate2)

# db.getCollection('company').find({"year_founded": {"$lt": "2000"}})  # works

################################################
#
# PRE = [
#     'US',
#     'TW',
# ]
# POST = [
#     'GB',
#     'HK',
# ]
#
#
# def get_country():
#     code, _ = locale.getlocale()
#     try:
#         return code.split('_')[1]
#     except IndexError:
#         raise Exception('Country cannot be ascertained from locale.')
#
#
# def get_leap_birthday(year):
#     country = get_country()
#     if country in PRE:
#         return datetime.date(year, 2, 28)
#     elif country in POST:
#         return datetime.date(year, 3, 1)
#     else:
#         raise Exception('It is unknown whether your country treats leap year '
#                       + 'birthdays as being on the 28th of February or '
#                       + 'the 1st of March. Please consult your country\'s '
#                       + 'legal code for in order to ascertain an answer.')
#
# def age(dob):
#     today = datetime.date.today()
#     years = today.year - dob.year
#
#     try:
#         birthday = datetime.date(today.year, dob.month, dob.day)
#     except ValueError as e:
#         if dob.month == 2 and dob.day == 29:
#             birthday = get_leap_birthday(today.year)
#         else:
#             raise e
#
#     if today < birthday:
#         years -= 1
#     return years
#
# print(age(datetime.date(1988, 2, 29)))


