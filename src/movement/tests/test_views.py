from django.contrib.auth.models import User
from django.test import TestCase


class MovementViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_movement_page_returns_200(self):
        self.assertEqual(self.client.get("/movement/").status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/movement/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_search_returns_200(self):
        self.assertEqual(self.client.get("/movement/search/", {"search": ""}).status_code, 200)
