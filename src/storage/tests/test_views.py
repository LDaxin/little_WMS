from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from storage.models import Storage, StorageType


class StorageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_pages_return_200(self):
        urls = [
            "/storage/regal/",
            "/storage/regal/add/modal",
            "/storage/regal/del/modal",
            f"/storage/regal/{self.storage.pk}",
            f"/storage/regal/{self.storage.pk}/i",
            "/storage/regal/search?search=",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/storage/regal/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_add_storage(self):
        response = self.client.post(
            "/storage/regal/add", {"name": "Regal B", "parent": "", "code": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Storage.objects.filter(name="Regal B").exists())

    def test_update_storage(self):
        response = self.client.post(
            f"/storage/regal/{self.storage.pk}/update",
            {"name": "Regal A2", "parent": "", "code": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.storage.refresh_from_db()
        self.assertEqual(self.storage.name, "Regal A2")

    def test_delete_storage(self):
        response = self.client.post(
            "/storage/regal/del", {f"_{self.storage.pk}": str(self.storage.pk)}
        )
        self.assertEqual(response.status_code, 200)
        # SoftDeleteManager.filter(pk=...) intentionally includes soft-deleted
        # rows, so the filtered queryset is used here (see softdelete/models.py).
        self.assertFalse(Storage.objects.all().filter(pk=self.storage.pk).exists())

    def test_export_storages(self):
        response = self.client.post(
            "/storage/regal/export", {f"_{self.storage.pk}": str(self.storage.pk)}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=iso-8859-1")


class StorageContentsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_store_in_storage(self):
        response = self.client.post(
            f"/storage/regal/{self.storage.pk}/store",
            {"code": self.article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.stored, self.storage.space)

    def test_store_in_storage_unknown_code(self):
        response = self.client.post(
            f"/storage/regal/{self.storage.pk}/store",
            {"code": "a0doesnotexist"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No article with that code")

    def test_remove_from_storage(self):
        self.article.stored = self.storage.space
        self.article.save()
        response = self.client.post(
            f"/storage/regal/{self.storage.pk}/remove/{self.article.pk}"
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertIsNone(self.article.stored)
