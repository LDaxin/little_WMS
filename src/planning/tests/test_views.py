from django.contrib.auth.models import Permission, User
from django.test import TestCase

from occasion.models import Occasion, OccasionType
from organisation.models import Role, UserProfile
from planning.models import CalendarEntry


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class CalendarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.occ_type = OccasionType.objects.create(name="Camp")

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_lists_entries_grouped_by_month(self):
        CalendarEntry.objects.create(title="Sommerlager", start_date="2026-07-01")
        CalendarEntry.objects.create(title="Herbstfahrt", start_date="2026-10-10")
        response = self.client.get("/calendar/")
        self.assertContains(response, "Sommerlager")
        self.assertContains(response, "Herbstfahrt")
        self.assertContains(response, "July 2026")
        self.assertContains(response, "October 2026")

    def test_occasion_entry_links(self):
        entry = CalendarEntry.objects.create(title="Sommerlager", start_date="2026-07-01")
        occasion = Occasion.objects.create(calendar_entry=entry, occasion_type=self.occ_type)
        response = self.client.get("/calendar/")
        self.assertContains(response, "/occasions/%s/" % occasion.pk)

    def test_permission(self):
        user_with("nobody", "article_view_all")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/calendar/").status_code, 403)
