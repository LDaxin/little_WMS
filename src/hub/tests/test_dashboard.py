from datetime import date

from django.contrib.auth.models import Permission, User
from django.test import TestCase

from notifications.services import notify
from organisation.models import Organisation, Role, UserProfile
from planning.models import CalendarEntry


def user_with(organisation, username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation=organisation, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, organisation=organisation, role=role)
    return user


class DashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")

    def test_requires_login(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_widgets_with_permission(self):
        user = user_with(
            self.org, "u",
            "article_view_all", "notification_view_all", "occasion_view_all", "settings_view_all",
        )
        self.client.login(username="u", password="pw")
        notify(user, "Hello")
        response = self.client.get("/dashboard/")
        self.assertContains(response, "Notifications")
        self.assertContains(response, "Hello")
        self.assertContains(response, "Statistics")

    def test_widgets_hidden_without_permission(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        response = self.client.get("/dashboard/")
        self.assertNotContains(response, "Statistics")
        self.assertNotContains(response, "Notifications")

    def test_alerts_from_checks(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen", start_date=date.today(), organisation=self.org
        )
        self.assertContains(self.client.get("/dashboard/"), "Maintenance due: Sharpen")

    def test_view_widget_shown(self):
        from savedviews.models import SavedView

        user = user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        SavedView.objects.create(
            owner=user, name="My widget", typ="tent", organisation=self.org,
            show_on_dashboard=True, query={"type": "AND", "conditions": []},
        )
        self.assertContains(self.client.get("/dashboard/"), "My widget")

    def test_view_widget_hidden(self):
        from savedviews.models import SavedView

        user = user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        SavedView.objects.create(
            owner=user, name="Hidden widget", typ="tent", organisation=self.org,
            show_on_dashboard=False,
        )
        self.assertNotContains(self.client.get("/dashboard/"), "Hidden widget")
