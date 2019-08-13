import datetime
import dateutil.parser
import jdatetime
from dateutil import tz, parser
import time

__author__ = 'R.Azh'
_date = dateutil.parser.parse('1981-08-24 00:00:00')
print(_date)

# adding timezone
utc_date = _date.replace(tzinfo=tz.gettz('UTC'))
print(utc_date)
local_date = utc_date.astimezone(tz.gettz(
        'America/New_York')).date()
print(local_date)

print(tz.gettz('Asia/Tehran'))  # Iran standard time

tehran_date = utc_date.astimezone(tz.gettz('IRST'))     # Iran standard time
print(tehran_date)

utc_date = datetime.datetime.utcnow().isoformat()
print(utc_date)
utc_date = dateutil.parser.parse(utc_date).replace(tzinfo=datetime.timezone.utc)
tehran_date = utc_date.astimezone(tz.gettz('Asia/Tehran')).strftime('%Y-%m-%dT%H:%M:%S')
print(tehran_date)

local_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
print(local_time)

# removing timezone
dt = utc_date.replace(tzinfo=None)


local_isoformat = datetime.date.today().strftime('%Y-%m-%dT00:00:00')
print('local isoformat: ', local_isoformat)
value = datetime.datetime.strptime(local_isoformat[:19], '%Y-%m-%dT%H:%M:%S')
value1 = value.replace(tzinfo=datetime.timezone.utc) # dont work
print(value1)
local_time = value.replace(tzinfo=tz.gettz('Asia/Tehran')) # dont work
utc_time = local_time.astimezone(datetime.timezone.utc)
print(utc_time)


def get_timestamp_in_milliseconds(date_time):
    return int(time.mktime(date_time.timetuple())) * 1000 + int(date_time.microsecond / 1000)


def get_timestamp_from_datetime(date_time):
    if type(date_time) is str:
        date_time = parser.parse(date_time)
    return int(time.mktime(date_time.timetuple()))


def get_datetime_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def utc_isoformat_from_timestamp(value):
    return datetime.datetime.utcfromtimestamp(value).strftime('%Y-%m-%dT%H:%M:%S')


def local_isoformat_from_timestamp(value):
    return datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%dT%H:%M:%S')


def datetime_from_isoformat(value):
    return dateutil.parser.parse(value)


def _utc_from_local(date_time):
    local_time = date_time.replace(tzinfo=tz.gettz('Asia/Tehran'))
    return local_time.astimezone(datetime.timezone.utc)


def _local_from_utc(date_time):
    utc_time = date_time.replace(tzinfo=datetime.timezone.utc)
    return utc_time.astimezone(tz.gettz('Asia/Tehran'))


def utc_isoformat_from_local_isoformat(value: object) -> object:
    return datetime.datetime.strftime(
        _utc_from_local(datetime_from_isoformat(value)),
        '%Y-%m-%dT%H:%M:%S'
    )


def utc_isoformat_from_local_datetime(value):
    return datetime.datetime.strftime(_utc_from_local(value), '%Y-%m-%dT%H:%M:%S')


def local_isoformat_from_utc_datetime(value):
    return datetime.datetime.strftime(_local_from_utc(value), '%Y-%m-%dT%H:%M:%S')


def local_isoformat_from_utc_isoformat(value):
    return datetime.datetime.strftime(
        _local_from_utc(datetime_from_isoformat(value)),
        '%Y-%m-%dT%H:%M:%S'
    )


def isoformat_from_datetime(value):
    return datetime.datetime.strftime(value, '%Y-%m-%dT%H:%M:%S')


def utc_timestamp_from_utc_isoformat(value):
    value = datetime.datetime.strptime(value[:19], '%Y-%m-%dT%H:%M:%S')
    value = value.replace(tzinfo=datetime.timezone.utc)
    return timestamp_from_epoch(value)


def timestamp_from_epoch(datetime_data):
    __EPOCH_NAIVE = datetime.datetime(1970, 1, 1)
    __EPOCH_AWARE = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    if datetime_data.tzinfo is None:
        return int((datetime_data - __EPOCH_NAIVE).total_seconds())
    else:
        return int((datetime_data - __EPOCH_AWARE).total_seconds())


date_time = datetime.datetime(year=2017, month=12, day=20,
                              hour=14, minute=50, second=48,
                              microsecond=256000)
timestamp_miliseconds = get_timestamp_in_milliseconds(date_time)
assert timestamp_miliseconds == 1513768848256
print(timestamp_miliseconds)
epoch_ts = timestamp_from_epoch(date_time)
print(epoch_ts)
timestamp = get_timestamp_from_datetime(date_time)
print(timestamp)
# assert epoch_ts == timestamp


utc_time = utc_isoformat_from_timestamp(epoch_ts)
local_time = local_isoformat_from_timestamp(epoch_ts)

print(utc_time)
print(local_time)

####################################################
def setUp(self):
    self.local_time = datetime.datetime(year=2018, month=5, day=30,
                               hour=10, minute=50, second=50)
    self.utc_time = datetime.datetime(year=2018, month=5, day=30,
                             hour=6, minute=20, second=50)
    self.local_time_isoformat = isoformat_from_datetime(self.local_time)
    self.utc_time_isoformat = isoformat_from_datetime(self.utc_time)


def test_utc_isoformat_from_local_isoformat(self):
    utc_iso_time = utc_isoformat_from_local_isoformat(self.local_time_isoformat)
    assert utc_iso_time == self.utc_time_isoformat


def test_utc_isoformat_from_local_datetime(self):
    utc_time = utc_isoformat_from_local_datetime(self.local_time)
    assert utc_time == self.utc_time_isoformat


def test_local_isoformat_from_utc_datetime(self):
    local_iso_time = local_isoformat_from_utc_datetime(self.utc_time)
    assert local_iso_time == self.local_time_isoformat


def test_local_isoformat_from_utc_isoformat(self):
    local_iso_time = local_isoformat_from_utc_isoformat(self.utc_time_isoformat)
    assert local_iso_time == self.local_time_isoformat

print('################ to jalali ########################33')

# import jalaali
#
# jalai_date = jalaali.Jalaali().to_jalaali(utc_date.year, utc_date.month, utc_date.day)
# print(jalai_date)
# local_date = datetime.date(jalai_date['jy'], jalai_date['jm'], jalai_date['jd'])
# print(local_date)


def calculate_utctime_from_tehran_time(base_time):
    tehran_date = base_time.replace(tzinfo=tz.gettz('IRST'))
    utc_date = tehran_date.astimezone(tz.gettz('UTC'))
    return utc_date


def test_calculate_utctime_from_tehran_time():
    date = jdatetime.datetime(year=1397, month=12, day=1).togregorian()
    utc_time = calculate_utctime_from_tehran_time(date)
    expected_utc_time = date - datetime.timedelta(seconds=12600)
    assert utc_time.year == expected_utc_time.year
    assert utc_time.month == expected_utc_time.month
    assert utc_time.day == expected_utc_time.day
    assert utc_time.hour == expected_utc_time.hour
    assert utc_time.minute == expected_utc_time.minute
    assert utc_time.second == expected_utc_time.second

    date = jdatetime.datetime(year=1397, month=5, day=1).togregorian()
    utc_time = calculate_utctime_from_tehran_time(date)
    expected_utc_time = date - datetime.timedelta(seconds=16200)
    assert utc_time.year == expected_utc_time.year
    assert utc_time.month == expected_utc_time.month
    assert utc_time.day == expected_utc_time.day
    assert utc_time.hour == expected_utc_time.hour
    assert utc_time.minute == expected_utc_time.minute
    assert utc_time.second == expected_utc_time.second


test_calculate_utctime_from_tehran_time()