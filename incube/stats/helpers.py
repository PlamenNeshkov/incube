from django.db.models import Avg
from collections import defaultdict

def average_latency(log_entries):
    return log_entries.aggregate(Avg('latency'))['latency__avg']

def unique_consumers(log_entries):
    return log_entries.exclude(consumer__isnull=True)\
        .values('consumer').distinct().count()

def all_time_calls(log_entries):
    return log_entries.count()

def hourly_calls_by_minute(log_entries, now):
    xs = log_entries.filter(
        created__year=now.year,
        created__month=now.month,
        created__day=now.day,
        created__hour=now.hour
    ).values('created')

    by_minute = defaultdict(int)
    for log_entry in xs:
        d = log_entry['created']
        by_minute[d.minute] += 1
    return (dict(by_minute), xs.count())

def daily_calls_by_hour(log_entries, now):
    xs = log_entries.filter(
        created__year=now.year,
        created__month=now.month,
        created__day=now.day
    ).values('created')

    by_hour = defaultdict(int)
    for log_entry in xs:
        d = log_entry['created']
        by_hour[d.hour] += 1
    return (dict(by_hour), xs.count())

def monthly_calls_by_day(log_entries, now):
    xs = log_entries.filter(
        created__year=now.year,
        created__month=now.month
    ).values('created')

    by_day = defaultdict(int)
    for log_entry in xs:
        d = log_entry['created']
        by_day[d.day] += 1
    return (dict(by_day), xs.count())

def yearly_calls_by_month(log_entries, now):
    xs = log_entries.filter(
        created__year=now.year
    ).values('created')

    by_month = defaultdict(int)
    for log_entry in xs:
        d = log_entry['created']
        by_month[d.month] += 1
    return (dict(by_month), xs.count())

def minute_calls(log_entries, now):
    xs = log_entries.filter(
        created__year=now.year,
        created__month=now.month,
        created__day=now.day,
        created__hour=now.hour,
        created__minute=now.minute
    )
    return xs.count()
