from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from storage.models import Storage, StorageType


class AllArticlesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="tent", symbol="TZ")
        base = ArticleBase.objects.create(name="Jurte", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_articles_all(self):
        self.assertEqual(self.client.get("/article/").status_code, 200)

    def test_search_all(self):
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jurte")

    def test_search_all_links_to_detail(self):
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertContains(response, "/article/tent/%s" % self.article.pk)

    def test_search_all_groups_by_location(self):
        storage_type = StorageType.objects.create(name="room", symbol="RA")
        first = Storage.objects.create(name="Regal A", typ=storage_type)
        second = Storage.objects.create(name="Regal B", typ=storage_type)
        Stock.objects.create(article=self.article, stored=first.space, menge=2)
        Stock.objects.create(article=self.article, stored=second.space, menge=1)
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertContains(response, "Regal A")
        self.assertContains(response, "Regal B")

    def test_search_all_single_location_one_row(self):
        storage_type = StorageType.objects.create(name="room", symbol="RA")
        storage = Storage.objects.create(name="Regal A", typ=storage_type)
        Stock.objects.create(article=self.article, stored=storage.space, menge=2)
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertContains(response, "Regal A")
        self.assertContains(response, "table-group-single")

    def test_search_all_sorts_by_name(self):
        article_type = ArticleType.objects.get(name="tent")
        Article.objects.create(base=ArticleBase.objects.create(name="Alpha", pType=article_type))
        content = self.client.get("/article/search", {"sort": "name"}).content.decode()
        self.assertLess(content.index("Alpha"), content.index("Jurte"))

    def test_search_all_sorts_descending(self):
        article_type = ArticleType.objects.get(name="tent")
        Article.objects.create(base=ArticleBase.objects.create(name="Alpha", pType=article_type))
        content = self.client.get("/article/search", {"sort": "-name"}).content.decode()
        self.assertLess(content.index("Jurte"), content.index("Alpha"))
