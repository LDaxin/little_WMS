from datetime import date

from django.test import TestCase

from planning.models import RecurrenceRule
from planning.services import add_months, recurrence_dates, step


class DateStepTest(TestCase):
    def test_add_months_clamps_day(self):
        self.assertEqual(add_months(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(add_months(date(2024, 1, 31), 1), date(2024, 2, 29))  # leap year
        self.assertEqual(add_months(date(2026, 1, 15), 1), date(2026, 2, 15))

    def test_step(self):
        self.assertEqual(step(date(2026, 1, 1), "daily", 2), date(2026, 1, 3))
        self.assertEqual(step(date(2026, 1, 1), "weekly", 1), date(2026, 1, 8))
        self.assertEqual(step(date(2026, 1, 31), "monthly", 1), date(2026, 2, 28))
        self.assertEqual(step(date(2026, 1, 1), "yearly", 1), date(2027, 1, 1))

    def test_recurrence_dates_end_after_occurrences(self):
        rule = RecurrenceRule(frequency="yearly", interval=1, end_after_occurrences=3)
        self.assertEqual(
            recurrence_dates(date(2026, 7, 1), rule),
            [date(2027, 7, 1), date(2028, 7, 1)],
        )

    def test_recurrence_dates_end_date(self):
        rule = RecurrenceRule(frequency="yearly", interval=1, end_date=date(2028, 12, 31))
        self.assertEqual(
            recurrence_dates(date(2026, 7, 1), rule),
            [date(2027, 7, 1), date(2028, 7, 1)],
        )

    def test_recurrence_dates_never_is_bounded(self):
        rule = RecurrenceRule(frequency="yearly", interval=1)
        dates = recurrence_dates(date(2026, 7, 1), rule)
        self.assertTrue(dates)
        self.assertLessEqual(dates[-1], date(2028, 7, 1))
