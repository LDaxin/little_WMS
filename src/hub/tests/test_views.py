from django.contrib.auth.models import User
from django.test import TestCase


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
