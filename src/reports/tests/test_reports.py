from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from article.models import Article
from audit.models import AuditLog
from organisation.models import Organisation, Role, UserProfile


def user_with(organisation, username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation=organisation, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, organisation=organisation, role=role)
    return user


class ReportsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")

    def test_requires_permission(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/reports/").status_code, 403)

    def test_reports_view(self):
        user_with(self.org, "u", "settings_view_all")
        self.client.login(username="u", password="pw")
        self.assertEqual(self.client.get("/reports/").status_code, 200)

    def test_movements_shown(self):
        user = user_with(self.org, "u", "settings_view_all")
        self.client.login(username="u", password="pw")
        article_ct = ContentType.objects.get_for_model(Article)
        AuditLog.objects.create(action="moved", content_type=article_ct, object_id=1, user=user)
        response = self.client.get("/reports/")
        self.assertContains(response, "Movements over time")
        self.assertContains(response, user.username)

    def test_csv_export(self):
        user_with(self.org, "u", "settings_view_all")
        self.client.login(username="u", password="pw")
        response = self.client.get("/reports/export.csv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn("month", response.content.decode())
