from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from planning.models import CalendarEntry, RecurrenceRule
from occasion.models import Occasion, OccasionType, Packlist
from organisation.models import Role, UserProfile


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class OccasionRecurrenceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.occ_type = OccasionType.objects.create(name="Camp")
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def _occasion(self):
        entry = CalendarEntry.objects.create(title="Summer", start_date="2026-07-01")
        return Occasion.objects.create(calendar_entry=entry, occasion_type=self.occ_type)

    def test_repeat_generates_instances_and_copies_packlist(self):
        occasion = self._occasion()
        Packlist.objects.create(occasion=occasion, article=self.article, quantity=4)

        self.client.post(
            "/occasions/%s/repeat/" % occasion.pk,
            {"frequency": "yearly", "interval": "1", "end_after_occurrences": "3"},
        )

        occasion.calendar_entry.refresh_from_db()
        rule = occasion.calendar_entry.recurrence_rule
        self.assertIsNotNone(rule)
        instances = Occasion.objects.filter(calendar_entry__recurrence_rule=rule)
        self.assertEqual(instances.count(), 3)  # head + 2
        for instance in instances:
            self.assertEqual(instance.packlist.get().quantity, 4)

    def test_already_recurring_guard(self):
        occasion = self._occasion()
        self.client.post(
            "/occasions/%s/repeat/" % occasion.pk,
            {"frequency": "yearly", "end_after_occurrences": "2"},
        )
        self.client.post(
            "/occasions/%s/repeat/" % occasion.pk,
            {"frequency": "monthly", "end_after_occurrences": "2"},
        )
        self.assertEqual(RecurrenceRule.objects.count(), 1)

    def test_repeat_permission(self):
        occasion = self._occasion()
        user_with("helper", "occasion_view_all")
        self.client.login(username="helper", password="pw")
        response = self.client.post(
            "/occasions/%s/repeat/" % occasion.pk, {"frequency": "yearly"}
        )
        self.assertEqual(response.status_code, 403)
