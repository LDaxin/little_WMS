from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from organisation.models import Role, UserProfile
from planning.models import CalendarEntry


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class MaintenanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hammer", pType=article_type)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")
        self.article = Article.objects.create(base=self.base)

    def test_add_maintenance(self):
        self.client.post(
            "/article/werkzeug/%s/maintenance" % self.article.pk,
            {"title": "Sharpen", "due_date": "2026-08-01"},
        )
        entry = CalendarEntry.objects.filter(article=self.article).first()
        self.assertIsNotNone(entry)
        self.assertEqual(entry.entry_type, "maintenance")
        self.assertEqual(entry.title, "Sharpen")
        self.assertEqual(str(entry.start_date), "2026-08-01")

    def test_maintenance_in_mini_calendar(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen", start_date="2026-08-01", article=self.article
        )
        response = self.client.get("/article/werkzeug/%s" % self.article.pk)
        self.assertContains(response, "Maintenance: Sharpen")

    def test_maintenance_in_calendar(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen", start_date="2026-08-01", article=self.article
        )
        self.assertContains(self.client.get("/calendar/"), "Sharpen")

    def test_permission(self):
        user_with("helper", "article_view_all")
        self.client.login(username="helper", password="pw")
        response = self.client.post(
            "/article/werkzeug/%s/maintenance" % self.article.pk,
            {"title": "Sharpen", "due_date": "2026-08-01"},
        )
        self.assertEqual(response.status_code, 403)
