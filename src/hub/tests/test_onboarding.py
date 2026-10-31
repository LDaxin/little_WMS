from django.contrib.auth.models import User
from django.test import TestCase

from article.models import ArticleType
from hub.models import Settings
from storage.models import StorageType


class OnboardingTest(TestCase):
    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_wizard(self):
        self.assertEqual(self.client.get("/onboarding/").status_code, 200)

    def test_apply(self):
        self.client.post("/onboarding/", {
            "article_tent": "on", "storage_building": "on", "role_templates": "on",
        })
        self.assertTrue(ArticleType.objects.filter(name="tent").exists())
        self.assertTrue(StorageType.objects.filter(name="building").exists())
        self.assertTrue(Settings.objects.first().onboarding_completed)

    def test_skip(self):
        self.client.post("/onboarding/", {"skip": "1"})
        self.assertFalse(ArticleType.objects.exists())
        self.assertTrue(Settings.objects.first().onboarding_completed)
