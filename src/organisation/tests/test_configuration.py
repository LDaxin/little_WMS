from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import ArticleType
from organisation.models import Role, UserProfile
from storage.models import StorageType


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class ConfigurationTest(TestCase):
    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_create_article_type(self):
        self.client.post("/configuration/", {"action": "article_type", "name": "tent", "symbol": "TZ"})
        self.assertTrue(ArticleType.objects.filter(name="tent").exists())

    def test_create_storage_type(self):
        self.client.post("/configuration/", {"action": "storage_type", "name": "room", "symbol": "RA"})
        self.assertTrue(StorageType.objects.filter(name="room").exists())

    def test_load_defaults(self):
        self.client.post("/configuration/", {"action": "load_defaults"})
        self.assertTrue(ArticleType.objects.filter(name="tent").exists())
        self.assertTrue(StorageType.objects.filter(name="building").exists())

    def test_create_role_templates(self):
        self.client.post("/configuration/", {"action": "role_templates"})
        self.assertTrue(Role.objects.filter(name="Full Access", is_template=True).exists())

    def test_permission(self):
        user_with("nobody", "article_view_all")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/configuration/").status_code, 403)
