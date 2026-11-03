from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from storage.models import Storage, StorageType


class AllArticlesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="tent", symbol="TZ")
        cls.base = ArticleBase.objects.create(name="Jurte", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def _stock(self, article, name=None, menge=1):
        if name is None:
            return Stock.objects.create(article=article, stored=None, menge=menge)
        storage_type, _ = StorageType.objects.get_or_create(name="room", symbol="RA")
        storage = Storage.objects.create(name=name, typ=storage_type)
        return Stock.objects.create(article=article, stored=storage.space, menge=menge)

    def test_articles_all(self):
        self.assertEqual(self.client.get("/article/").status_code, 200)

    def test_search_all(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jurte")

    def test_search_all_links_to_detail(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertContains(response, "/article/tent/%s" % self.article.pk)

    def test_search_all_groups_by_location(self):
        self._stock(self.article, "Regal A", 2)
        self._stock(self.article, "Regal B", 1)
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertContains(response, "Regal A")
        self.assertContains(response, "Regal B")

    def test_search_all_single_location_one_row(self):
        self._stock(self.article, "Regal A", 2)
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertContains(response, "Regal A")
        self.assertContains(response, "table-group-single")

    def test_search_all_sorts_by_name(self):
        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        content = self.client.get("/article/search", {"sort": "name"}).content.decode()
        self.assertLess(content.index("Alpha"), content.index("Jurte"))

    def test_search_all_sorts_descending(self):
        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        content = self.client.get("/article/search", {"sort": "-name"}).content.decode()
        self.assertLess(content.index("Jurte"), content.index("Alpha"))

    def test_search_all_selects_columns(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"cols": "name,quantity"})
        self.assertContains(response, "Quantity")
        self.assertNotContains(response, "Condition")

    def test_search_all_hides_stock_rows_without_stock_columns(self):
        self._stock(self.article, "Regal A", 2)
        self._stock(self.article, "Regal B", 1)
        response = self.client.get("/article/search", {"cols": "name,code"})
        self.assertNotContains(response, "Regal A")

    def test_search_all_cards_mode(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"mode": "cards"})
        self.assertContains(response, "card-title")

    def test_search_all_table_mode(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"mode": "table"})
        self.assertContains(response, "resultsTable")
