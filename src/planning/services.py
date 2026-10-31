"""Recurrence date arithmetic (§2). No external dependency."""
import calendar as _calendar
from datetime import timedelta

# How far a "never" rule generates ahead (days). ~2 years.
RECURRENCE_HORIZON_DAYS = 730


def add_months(date, months):
    """Add ``months`` to ``date``, clamping the day to the month's last day."""
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, _calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)


def step(date, frequency, interval):
    """The next date after ``date`` for one recurrence step."""
    if frequency == "daily":
        return date + timedelta(days=interval)
    if frequency == "weekly":
        return date + timedelta(weeks=interval)
    if frequency == "monthly":
        return add_months(date, interval)
    if frequency == "yearly":
        return add_months(date, 12 * interval)
    raise ValueError("unknown frequency: %s" % frequency)


def recurrence_dates(start, rule):
    """The dates of the instances AFTER the head, bounded by the rule.

    ``end_after_occurrences`` counts the head as the first occurrence.
    """
    dates = []
    current = start
    count = 1  # the head
    while True:
        current = step(current, rule.frequency, rule.interval)
        if rule.end_date and current > rule.end_date:
            break
        if rule.end_after_occurrences and count >= rule.end_after_occurrences:
            break
        if (
            not rule.end_date
            and not rule.end_after_occurrences
            and current > start + timedelta(days=RECURRENCE_HORIZON_DAYS)
        ):
            break
        dates.append(current)
        count += 1
    return dates
