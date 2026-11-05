from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase

from article.calendar import calendar_items, month_grid
from article.models import Article, ArticleBase, ArticleType
from organisation.models import UserProfile
from planning.models import CalendarEntry


def _this_month(day):
    """A day in the current month (the months the module shows initially)."""
    today = date.today()
    return date(today.year, today.month, 1) + timedelta(days=day)


def _item(ident, start, end, title="Term"):
    return {"id": ident, "type": "maintenance", "title": title, "start": start,
            "end": end, "color": "#000000", "entry": None, "url": ""}


class MonthGridTest(TestCase):
    def test_range_becomes_a_bar_and_single_day_a_dot(self):
        items = [
            _item("a", date(2026, 7, 1), date(2026, 7, 3), "Range"),
            _item("b", date(2026, 7, 10), date(2026, 7, 10), "Single"),
        ]
        grid = month_grid(2026, 7, items, today=date(2026, 7, 15))
        segments = [seg for week in grid["weeks"] for seg in week["segments"]]
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["col_e"] - segments[0]["col_s"], 2)
        self.assertEqual(segments[0]["lane"], 0)
        dots = [dot for week in grid["weeks"] for cell in week["cells"] for dot in cell["dots"]]
        self.assertEqual(len(dots), 1)

    def test_overlapping_bars_stack_in_lanes(self):
        items = [
            _item("a", date(2026, 7, 1), date(2026, 7, 5)),
            _item("b", date(2026, 7, 3), date(2026, 7, 7)),
        ]
        grid = month_grid(2026, 7, items, today=date(2026, 7, 15))
        week = next(w for w in grid["weeks"] if len(w["segments"]) == 2)
        lanes = {seg["item"]["id"]: seg["lane"] for seg in week["segments"]}
        self.assertEqual(lanes, {"a": 0, "b": 1})


class DetailCalendarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)

    def setUp(self):
        user = User.objects.create_superuser("boss", "b@e.st", "pw")
        UserProfile.objects.create(user=user, organisation_id=1)
        self.client.login(username="boss", password="pw")
        self.article = Article.objects.create(base=self.base)

    def _detail(self, **params):
        from urllib.parse import urlencode

        url = "/article/werkzeug/%s" % self.article.pk
        if params:
            url += "?" + urlencode(params)
        return self.client.get(url)

    def test_grid_shows_a_bar_for_a_range(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Repair",
            start_date=_this_month(1), end_date=_this_month(5), article=self.article,
        )
        response = self._detail()
        self.assertContains(response, "cal-bar")
        self.assertContains(response, "Repair")

    def test_grid_shows_a_dot_for_a_single_day(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen",
            start_date=_this_month(3), article=self.article,
        )
        self.assertContains(self._detail(), "cal-dot")

    def test_switch_to_list_shows_the_list(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen",
            start_date=_this_month(3), article=self.article,
        )
        response = self._detail(calendar_view="list")
        self.assertContains(response, "Maintenance: Sharpen")

    def test_switch_persists_the_profile_setting(self):
        self.client.post(
            "/article/werkzeug/%s/calendar" % self.article.pk, {"view": "list"}
        )
        profile = UserProfile.objects.get(user__username="boss")
        self.assertEqual(profile.detail_calendar_view, "list")

    def test_month_endpoint_returns_a_block_and_a_sentinel(self):
        response = self.client.get(
            "/article/werkzeug/%s/calendar/month?year=2026&month=7&dir=next" % self.article.pk,
            HTTP_HX_REQUEST="true",
        )
        self.assertContains(response, "cal-month")
        self.assertContains(response, "cal-sentinel-bottom")

    def test_conflict_check_reports_an_overlap(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Repair",
            start_date="2026-07-01", end_date="2026-07-05", article=self.article,
        )
        response = self.client.get(
            "/article/werkzeug/%s/calendar/check?start=2026-07-03&end=2026-07-04" % self.article.pk,
            HTTP_HX_REQUEST="true",
        )
        self.assertContains(response, "Reservation")

    def test_conflict_check_offers_actions_when_free(self):
        response = self.client.get(
            "/article/werkzeug/%s/calendar/check?start=2030-01-01&end=2030-01-02" % self.article.pk,
            HTTP_HX_REQUEST="true",
        )
        self.assertContains(response, "action=maintenance")

    def test_entry_can_be_edited_and_deleted(self):
        entry = CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen", start_date="2026-08-01", article=self.article
        )
        ident = "entry-%s" % entry.pk
        self.client.post(
            "/article/werkzeug/%s/calendar/entry/save" % self.article.pk,
            {"entry": ident, "title": "Sharpen2", "start": "2026-08-02", "end": ""},
            HTTP_HX_REQUEST="true",
        )
        entry.refresh_from_db()
        self.assertEqual(entry.title, "Sharpen2")
        self.assertEqual(str(entry.start_date), "2026-08-02")
        self.client.post(
            "/article/werkzeug/%s/calendar/entry/delete" % self.article.pk,
            {"entry": ident}, HTTP_HX_REQUEST="true",
        )
        remaining = [item for item in calendar_items(self.article) if item["id"] == ident]
        self.assertEqual(remaining, [])
