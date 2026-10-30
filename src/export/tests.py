from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from storage.models import Storage, StorageType


class QRPrintTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def test_requires_login(self):
        self.client.logout()
        response = self.client.post("/qr/print", {"type": "article"})
        self.assertEqual(response.status_code, 302)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get("/qr/print").status_code, 404)

    def test_print_articles(self):
        response = self.client.post(
            "/qr/print",
            {"type": "article", f"_{self.article.pk}": str(self.article.pk)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<svg")
        self.assertContains(response, "Hammer")

    def test_print_storages(self):
        response = self.client.post(
            "/qr/print",
            {"type": "storage", f"_{self.storage.pk}": str(self.storage.pk)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<svg")
        self.assertContains(response, "Regal A")

    def test_label_code_hides_name(self):
        response = self.client.post(
            "/qr/print",
            {"type": "article", "label": "code", f"_{self.article.pk}": str(self.article.pk)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Hammer")

    def test_link_content(self):
        response = self.client.post(
            "/qr/print",
            {"type": "article", "qr": "link", f"_{self.article.pk}": str(self.article.pk)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<svg")
