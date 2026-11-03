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

    def test_search_all_cards_have_checkbox(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"mode": "cards"})
        self.assertContains(response, "card-check")

    def test_search_all_sorts_by_quantity(self):
        self._stock(self.article, "Regal A", 5)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha, "Regal B", 1)
        content = self.client.get("/article/search", {"sort": "quantity"}).content.decode()
        self.assertLess(content.index("Alpha"), content.index("Jurte"))

    def test_search_all_advanced_query_filters(self):
        import json

        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        query = json.dumps({"type": "AND", "conditions": [
            {"field": "base__name", "op": "contains", "value": "Jurte"}]})
        response = self.client.get("/article/search", {"query": query})
        self.assertContains(response, "Jurte")
        self.assertNotContains(response, "Alpha")

    def test_search_all_renders_state_inputs(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"sort": "name", "cols": "name,code"})
        self.assertContains(response, 'id="sortInput" name="sort" value="name"')
        self.assertContains(response, 'id="colsInput" name="cols" value="name,code"')

    def test_search_all_paginates(self):
        for i in range(51):
            base = ArticleBase.objects.create(name="Item %03d" % i, pType=self.article_type)
            self._stock(Article.objects.create(base=base))
        response = self.client.get("/article/search")
        self.assertContains(response, "listControl")
        self.assertContains(response, "page=2")

    def test_search_all_append_rows_only(self):
        self._stock(self.article)
        response = self.client.get("/article/search", {"append": "1"})
        self.assertNotContains(response, "resultsTable")
        self.assertContains(response, "Jurte")

    def test_select_all_control_present(self):
        response = self.client.get("/article/tent/")
        self.assertContains(response, "selectAllButton")

    def test_bulk_delete_all_matches(self):
        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        response = self.client.post("/article/tent/del", {"all": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.all().filter(pk=self.article.pk).exists())
        self.assertFalse(Article.objects.all().filter(pk=alpha.pk).exists())

    def test_bulk_delete_all_matches_respects_search(self):
        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        self.client.post("/article/tent/del", {"all": "1", "search": "Jurte"})
        self.assertFalse(Article.objects.all().filter(pk=self.article.pk).exists())
        self.assertTrue(Article.objects.all().filter(pk=alpha.pk).exists())

    def test_bulk_export_all_matches(self):
        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        response = self.client.post("/article/tent/export", {"all": "1"})
        content = response.content.decode("iso-8859-1")
        self.assertIn("Jurte", content)
        self.assertIn("Alpha", content)

    def test_bulk_qr_all_matches(self):
        self._stock(self.article)
        alpha = Article.objects.create(
            base=ArticleBase.objects.create(name="Alpha", pType=self.article_type)
        )
        self._stock(alpha)
        response = self.client.post("/qr/print", {"type": "article", "typ": "tent", "all": "1"})
        self.assertContains(response, "Jurte")
        self.assertContains(response, "Alpha")

    def test_list_default_applies_on_mobile(self):
        self._stock(self.article)
        # the page must not pin an explicit mode — that would override the setting
        response = self.client.get("/article/tent/")
        self.assertContains(response, 'id="modeInput" name="mode" value=""')
        # a mobile client with no explicit mode gets the configured default (cards)
        response = self.client.get("/article/tent/search", HTTP_X_VIEW_MODE="mobile")
        self.assertContains(response, "card-title")

    def test_explicit_mode_wins_over_default(self):
        self._stock(self.article)
        response = self.client.get(
            "/article/tent/search", {"mode": "table"}, HTTP_X_VIEW_MODE="mobile"
        )
        self.assertContains(response, "resultsTable")
