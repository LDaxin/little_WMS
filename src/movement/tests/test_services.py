from django.core.exceptions import ValidationError
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from movement.services import MovementService, resolve_space
from movement.tests.test_movement import make_article
from storage.models import Storage, StorageType


class ResolveSpaceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.container_type = ArticleType.objects.create(
            name="Box", symbol="BX", article_toggle_space=True
        )
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def test_storage_code(self):
        self.assertEqual(resolve_space(self.storage.code.code), self.storage.space)

    def test_article_code(self):
        container = make_article("Box A", self.container_type, space_active=True)
        self.assertEqual(resolve_space(container.code.code), container.space)

    def test_unknown_code(self):
        with self.assertRaises(ValidationError):
            resolve_space("xx123")


class MovementServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.container_type = ArticleType.objects.create(
            name="Box", symbol="BX", article_toggle_space=True
        )
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def test_store_article(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        MovementService.store_article(article, self.storage.space)
        self.assertTrue(article.stocks.filter(stored=self.storage.space).exists())

    def test_store_article_in_container(self):
        container = make_article("Box A", self.container_type, space_active=True)
        article = make_article("Hammer", self.article_type, space_active=False)
        MovementService.store_article(article, container.space)
        self.assertTrue(article.stocks.filter(stored=container.space).exists())

    def test_store_article_in_itself_raises(self):
        container = make_article("Box A", self.container_type, space_active=True)
        with self.assertRaises(ValidationError):
            MovementService.store_article(container, container.space)

    def test_store_cycle_raises(self):
        a = make_article("Box A", self.container_type, space_active=True)
        b = make_article("Box B", self.container_type, space_active=True)
        MovementService.store_article(b, a.space)
        with self.assertRaises(ValidationError):
            MovementService.store_article(a, b.space)

    def test_store_articles_is_atomic(self):
        good = make_article("Hammer", self.article_type, space_active=False)
        bad = make_article("Box", self.container_type, space_active=True)
        with self.assertRaises(ValidationError):
            MovementService.store_articles([good, bad], bad.space)
        self.assertFalse(good.stocks.filter(stored=bad.space).exists())

    def test_remove_article(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=self.storage.space, menge=1)
        MovementService.remove_article(article)
        self.assertFalse(article.stocks.filter(stored=self.storage.space).exists())

    def _mergeable(self, menge):
        merge_type, _ = ArticleType.objects.get_or_create(
            name="Perlen", defaults={"symbol": "PR", "allow_merge_split": True}
        )
        base, _ = ArticleBase.objects.get_or_create(name="Bügelperle", pType=merge_type)
        article = Article.objects.create(base=base)
        Stock.objects.create(article=article, stored=None, menge=menge)
        return article

    def test_store_mergeable_moves_all(self):
        article = self._mergeable(30)
        MovementService.store_article(article, self.storage.space)
        self.assertEqual(article.stocks.get(stored=self.storage.space).menge, 30)
        self.assertFalse(article.stocks.filter(stored=None).exists())

    def test_store_mergeable_partial(self):
        article = self._mergeable(100)
        MovementService.store_article(article, self.storage.space, amount=30)
        self.assertEqual(article.stocks.get(stored=self.storage.space).menge, 30)
        self.assertEqual(article.stocks.get(stored=None).menge, 70)

    def test_store_non_mergeable_moves_single_stock(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=None, menge=1)
        MovementService.store_article(article, self.storage.space)
        self.assertEqual(article.stocks.count(), 1)
        self.assertEqual(article.stocks.first().stored, self.storage.space)

    def test_store_does_not_merge_other_article(self):
        base = ArticleBase.objects.create(name="Hering", pType=self.article_type)
        first = Article.objects.create(base=base)
        Stock.objects.create(article=first, stored=self.storage.space, menge=1)
        second = Article.objects.create(base=base)
        MovementService.store_article(second, self.storage.space)
        self.assertEqual(
            Stock.objects.filter(stored=self.storage.space, article__base=base).count(), 2
        )
