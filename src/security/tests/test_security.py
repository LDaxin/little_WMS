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
