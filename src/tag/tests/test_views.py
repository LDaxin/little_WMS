from django.contrib.auth.models import User
from django.test import TestCase

from tag.models import Tag


class TagViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Werkzeug")

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_pages_return_200(self):
        urls = [
            "/tag/",
            f"/tag/{self.tag.pk}",
            f"/tag/{self.tag.pk}/i",
            "/tag/search?search=",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/tag/search?search=")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_add_tag(self):
        response = self.client.post("/tag/add", {"name": "Hammer", "parent": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tag.objects.filter(name="Hammer").exists())

    def test_update_tag(self):
        response = self.client.post(
            f"/tag/{self.tag.pk}/update", {"name": "Werkzeug2", "parent": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Werkzeug2")

    def test_delete_tag(self):
        response = self.client.post(
            "/tag/del", {f"_{self.tag.pk}": str(self.tag.pk)}
        )
        self.assertEqual(response.status_code, 200)
        # SoftDeleteManager.filter(pk=...) intentionally includes soft-deleted
        # rows, so the filtered queryset is used here (see softdelete/models.py).
        self.assertFalse(Tag.objects.all().filter(pk=self.tag.pk).exists())
