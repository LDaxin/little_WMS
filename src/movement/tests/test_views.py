from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from space.models import Space
from storage.models import Storage, StorageType


class MovementViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        # The add-article view creates a Space for every article; mirror that here.
        cls.article_space = Space.objects.create(prefix="a0", active=True)
        cls.article = Article.objects.create(base=cls.article_base, space=cls.article_space)
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

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

    def test_request_article_code(self):
        response = self.client.get("/movement/request/", {"code": self.article.code.code})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Hammer")

    def test_request_storage_code(self):
        response = self.client.get("/movement/request/", {"code": self.storage.code.code})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["storage"])

    def test_request_unknown_code(self):
        response = self.client.get("/movement/request/", {"code": "xx123"})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json()["error"], "")

    def test_search_returns_200(self):
        self.assertEqual(self.client.get("/movement/search/", {"search": ""}).status_code, 200)

    def test_store_article(self):
        response = self.client.post(
            "/movement/store/",
            {"storageCode": self.storage.code.code, "articleCode1": self.article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.stored, self.storage.space)

    def test_remove_article(self):
        self.article.stored = self.storage.space
        self.article.save()
        response = self.client.post(
            "/movement/remove/", {"articleCode1": self.article.code.code}
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertIsNone(self.article.stored)
