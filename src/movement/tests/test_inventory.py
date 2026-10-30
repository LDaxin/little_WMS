from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Stock
from movement.tests.test_movement import make_article
from storage.models import Storage, StorageType
from article.models import ArticleType


class InventoryTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def scan(self, code):
        return self.client.post("/inventory/scan/", {"code": code})

    def state(self):
        return self.client.session.get("inventory")


class InventoryViewTest(InventoryTestBase):
    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/inventory/").status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 302)

    def test_scan_location_sets_scope(self):
        self.scan(self.storage.code.code)
        self.assertEqual(self.state()["space"], self.storage.code.code)

    def test_scan_article_without_location_errors(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.scan(article.code.code)
        self.assertContains(response, "Scan a location first")

    def test_scan_article_marks_found(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=self.storage.space, menge=1)
        self.scan(self.storage.code.code)
        response = self.scan(article.code.code)
        self.assertContains(response, "1/1 scanned")

    def test_deviation_flagged(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        other = Storage.objects.create(name="Regal B", typ=self.storage_type)
        Stock.objects.create(article=article, stored=other.space, menge=1)
        self.scan(self.storage.code.code)
        response = self.scan(article.code.code)
        self.assertContains(response, "Deviations")
        self.assertContains(response, "Regal B")

    def test_clear_resets(self):
        self.scan(self.storage.code.code)
        self.client.post("/inventory/clear/")
        self.assertIsNone(self.state()["space"])

    def test_export_csv(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=self.storage.space, menge=1)
        self.scan(self.storage.code.code)
        response = self.client.get("/inventory/export/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn("Hammer", response.content.decode())

    def test_search_by_name(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.get("/inventory/search/", {"code": "Hammer"})
        self.assertContains(response, article.code.code)

    def test_search_empty(self):
        response = self.client.get("/inventory/search/", {"code": ""})
        self.assertEqual(response.status_code, 200)
