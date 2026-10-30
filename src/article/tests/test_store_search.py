from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from storage.models import Storage, StorageType


class StoreTargetSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)
        storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=storage_type)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_search_by_name(self):
        response = self.client.get(
            "/article/werkzeug/%s/store-search" % self.article.pk, {"code": "Regal"}
        )
        self.assertContains(response, self.storage.code.code)

    def test_detail_has_scanner_and_results(self):
        response = self.client.get("/article/werkzeug/%s" % self.article.pk)
        self.assertContains(response, "QRButtonstoreCode")
        self.assertContains(response, "storeResults")
