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
            "icon_size_desktop": "40",
            "icon_size_mobile": "20",
            "text_size_desktop": "18",
            "text_size_mobile": "12",
            "view_mode": "mobile",
        })
        profile = self.user.profiles.first()
        self.assertEqual(profile.sidebar_position_desktop, "right")
        self.assertEqual(profile.sidebar_position_mobile, "left")
        self.assertEqual(profile.icon_size_desktop, 40)
        self.assertEqual(profile.icon_size_mobile, 20)
        self.assertEqual(profile.text_size_desktop, 18)
        self.assertEqual(profile.text_size_mobile, 12)
        self.assertEqual(profile.view_mode, "mobile")

    def test_save_scan_feedback_settings(self):
        org = Organisation.objects.create(name="A", slug="a")
        UserProfile.objects.create(user=self.user, organisation=org)
        self.client.post("/email-preferences/", {
            "sound_enabled": "on",
            "image_on_scan": "on",
            "volume": "80",
        })
        profile = self.user.profiles.first()
        self.assertTrue(profile.sound_enabled)
        self.assertFalse(profile.vibration_enabled)
        self.assertTrue(profile.image_on_scan)
        self.assertEqual(profile.volume, 80)


class DefaultColumnsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", "u@example.com", "pw")
        self.client.login(username="u", password="pw")

    def test_save_default_columns(self):
        org = Organisation.objects.create(name="A", slug="a")
        UserProfile.objects.create(user=self.user, organisation=org)
        self.client.post("/list-columns/default/", {"list_type": "article", "cols": "name,code"})
        self.assertEqual(self.user.profiles.first().list_columns, {"article": ["name", "code"]})


class SidebarTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def test_sidebar_rendered(self):
        response = self.client.get("/")
        self.assertContains(response, 'class="sidebar')

    def test_text_size_scales_root_font(self):
        response = self.client.get("/")
        self.assertContains(response, "--text-desktop: 16px")
        self.assertContains(response, "font-size: var(--text-desktop")
