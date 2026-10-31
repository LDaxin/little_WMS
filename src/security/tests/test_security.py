from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase


class LoginRateLimitTest(TestCase):
    def setUp(self):
        cache.clear()
        User.objects.create_user("u", password="pw")

    def test_successful_login(self):
        response = self.client.post("/accounts/login/", {"username": "u", "password": "pw"})
        self.assertEqual(response.status_code, 302)

    def test_lockout_after_failures(self):
        for _ in range(5):
            self.client.post("/accounts/login/", {"username": "u", "password": "wrong"})
        response = self.client.post("/accounts/login/", {"username": "u", "password": "pw"})
        self.assertContains(response, "Too many failed attempts")

    def test_lockout_per_ip(self):
        for _ in range(5):
            self.client.post("/accounts/login/", {"username": "other", "password": "wrong"})
        response = self.client.post("/accounts/login/", {"username": "u", "password": "pw"})
        self.assertContains(response, "Too many failed attempts")


class HttpsSettingsTest(TestCase):
    def test_off_by_default(self):
        from django.conf import settings

        self.assertFalse(getattr(settings, "SESSION_COOKIE_SECURE", False))
        self.assertFalse(getattr(settings, "SECURE_SSL_REDIRECT", False))


class GdprTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", password="pw")
        self.client.login(username="u", password="pw")

    def test_export(self):
        response = self.client.get("/my-data/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "u")

    def test_delete_user_anonymises(self):
        from django.contrib.contenttypes.models import ContentType

        from article.models import Article
        from audit.models import AuditLog

        User.objects.create_superuser("boss", "b@e.st", "pw")
        article_ct = ContentType.objects.get_for_model(Article)
        log = AuditLog.objects.create(action="moved", content_type=article_ct, object_id=1, user=self.user)
        self.client.login(username="boss", password="pw")
        self.client.post("/users/%s/delete/" % self.user.pk)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        log.refresh_from_db()
        self.assertIsNone(log.user)

    def test_delete_permission(self):
        other = User.objects.create_user("other", password="pw")
        self.client.login(username="u", password="pw")
        self.assertEqual(self.client.post("/users/%s/delete/" % other.pk).status_code, 403)
