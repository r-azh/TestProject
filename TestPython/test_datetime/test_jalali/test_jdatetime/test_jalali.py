from datetime import datetime, date, timedelta, timezone

import jdatetime


fa_date = jdatetime.datetime.now()
print(fa_date)


fa_time = jdatetime.date.today()
print(fa_time)

fa_date = jdatetime.date(1397, 8, 6, locale='fa_IR')
print(fa_date)

fa_datetime = jdatetime.datetime(1397, 4, 23, 11, 40, 30, locale='fa_IR')
print(fa_datetime)
print(jdatetime.datetime(1397, 8, 21, 18, 00, 00).togregorian())

gregorian_date = datetime.utcnow()
fa_date = jdatetime.date.fromgregorian(date=gregorian_date)
print(gregorian_date)
print("week_day: ", gregorian_date.weekday())
print(fa_date)
print("fa_week_day: ", fa_date.weekday())

fa_datetime = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
print(fa_datetime)

print("gregorian: ", fa_datetime.togregorian())


import calendar
today = date.today()
month_start_of_week, month_days = calendar.monthrange(today.year, today.month)
print(month_start_of_week, month_days)

print(today)
next_month_start_time = today + timedelta(days=month_days - today.day + 1)
print(next_month_start_time)

print(jdatetime.j_days_in_month)
fa_time = jdatetime.date.today()
month_days = jdatetime.j_days_in_month[fa_time.month - 1]
print(month_days)

print(fa_time)
fa_next_month_start_time = fa_time + jdatetime.timedelta(days=month_days - fa_time.day + 1)
print(fa_next_month_start_time)

print(fa_next_month_start_time)
print(fa_next_month_start_time.month)
# fa_next_month_start_time.month = fa_next_month_start_time + 1   #dont work


print(today)
print(today.month)
# today.month += 1  #dont work

# to get gregorian utc time from jalali local time
print(today - timedelta(12600))   # -3.5 hours


class Month:
    def __init__(self, value):
        self.value = value


def calculate_next_first_of_month(base_time, leap, persian_calendar):
    if isinstance(leap, Month):
        base = base_time
        if persian_calendar:
            base = jdatetime.datetime.fromgregorian(date=base)
            for m in range(leap.value):
                days_in_month = jdatetime.j_days_in_month[base.month - 1]
                base = base + timedelta(days=days_in_month - base.day + 1)
            return base.togregorian()

        for m in range(leap.value):
            _, days_in_month = calendar.monthrange(base.year, base.month)
            base = base + timedelta(days=days_in_month - base.day + 1)
        return base


def get_local_tzinfo():
    local_timezone = datetime.now(timezone.utc).astimezone().tzinfo
    return local_timezone
