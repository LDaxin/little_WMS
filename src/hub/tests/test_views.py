from django.contrib.auth.models import User
from django.test import TestCase

from hub.mail import is_subscribed
from organisation.models import Organisation, UserProfile


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

    def test_save_language(self):
        org = Organisation.objects.create(name="A", slug="a")
        UserProfile.objects.create(user=self.user, organisation=org)
        self.client.post("/email-preferences/", {"language": "en"})
        self.assertEqual(self.user.profiles.first().language, "en")

    def test_save_sidebar_settings(self):
        org = Organisation.objects.create(name="A", slug="a")
        UserProfile.objects.create(user=self.user, organisation=org)
        self.client.post("/email-preferences/", {
            "sidebar_position_desktop": "right",
            "sidebar_position_mobile": "left",
            "icon_size_desktop": "large",
            "icon_size_mobile": "small",
            "text_size_desktop": "large",
            "text_size_mobile": "small",
            "view_mode": "mobile",
        })
        profile = self.user.profiles.first()
        self.assertEqual(profile.sidebar_position_desktop, "right")
        self.assertEqual(profile.sidebar_position_mobile, "left")
        self.assertEqual(profile.icon_size_desktop, "large")
        self.assertEqual(profile.icon_size_mobile, "small")
        self.assertEqual(profile.text_size_desktop, "large")
        self.assertEqual(profile.text_size_mobile, "small")
        self.assertEqual(profile.view_mode, "mobile")


class SidebarTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def test_sidebar_rendered(self):
        response = self.client.get("/")
        self.assertContains(response, 'class="sidebar')
