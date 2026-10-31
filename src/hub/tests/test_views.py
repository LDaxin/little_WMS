from django.contrib.auth.models import User
from django.test import TestCase

from hub.mail import is_subscribed


class HubViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def test_hub_returns_200(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_hub_requires_login(self):
        self.client.logout()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])


class EmailPreferencesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", "u@example.com", "pw")
        self.client.login(username="u", password="pw")

    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/email-preferences/").status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get("/email-preferences/").status_code, 302)

    def test_toggle_off(self):
        self.client.post("/email-preferences/", {})  # nothing checked
        self.assertFalse(is_subscribed(self.user, "notifications"))
        self.assertFalse(is_subscribed(self.user, "invitations"))

    def test_toggle_on(self):
        self.client.post("/email-preferences/", {"notifications": "on"})
        self.assertTrue(is_subscribed(self.user, "notifications"))
        self.assertFalse(is_subscribed(self.user, "invitations"))
