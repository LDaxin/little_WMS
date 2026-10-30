from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import ArticleType
from organisation.models import Role, UserProfile
from storage.models import StorageType


def user_with(username, *codenames):
    """A user whose role grants exactly the given catalogue permissions."""
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


# (url, method, permission) — one representative view per area
CASES = [
    ("/article/werkzeug/", "get", "article_view_all"),
    ("/storage/regal/", "get", "storage_view_all"),
    ("/tag/", "get", "tag_view_all"),
    ("/location/", "get", "location_view_all"),
    ("/code/", "get", "code_view_all"),
    ("/movement/", "get", "article_move_all"),
    ("/where/", "get", "article_view_all"),
    ("/inventory/", "get", "article_view_all"),
]


class EnforcementTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ArticleType.objects.create(name="werkzeug", symbol="WZ")
        StorageType.objects.create(name="regal", symbol="RG")

    def test_missing_permission_is_forbidden(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        for url, method, _ in CASES:
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, 403, "%s should be 403" % url)

    def test_granted_permission_allows(self):
        for i, (url, method, perm) in enumerate(CASES):
            user_with("user%d" % i, perm)
            self.client.login(username="user%d" % i, password="pw")
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, 200, "%s should be 200" % url)
            self.client.logout()

    def test_superuser_passes(self):
        User.objects.create_superuser("admin", "a@b.c", "pw")
        self.client.login(username="admin", password="pw")
        for url, method, _ in CASES:
            response = getattr(self.client, method)(url)
            self.assertEqual(response.status_code, 200, "%s should be 200" % url)

    def test_create_requires_create_permission(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.post("/article/werkzeug/add", {}).status_code, 403)

    def test_export_requires_export_permission(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.post("/qr/print", {"type": "article"}).status_code, 403)
