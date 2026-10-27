from django.core.exceptions import ValidationError
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
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
        article.refresh_from_db()
        self.assertEqual(article.stored, self.storage.space)

    def test_store_article_in_container(self):
        container = make_article("Box A", self.container_type, space_active=True)
        article = make_article("Hammer", self.article_type, space_active=False)
        MovementService.store_article(article, container.space)
        article.refresh_from_db()
        self.assertEqual(article.stored, container.space)

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
        good.refresh_from_db()
        self.assertIsNone(good.stored)

    def test_remove_article(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        article.stored = self.storage.space
        article.save()
        MovementService.remove_article(article)
        article.refresh_from_db()
        self.assertIsNone(article.stored)

    def test_store_merges_same_base(self):
        merge_type = ArticleType.objects.create(name="Perlen", symbol="PR", allow_merge_split=True)
        base = ArticleBase.objects.create(name="Bügelperle", pType=merge_type)
        existing = Article.objects.create(base=base, stored=self.storage.space, menge=50)
        incoming = Article.objects.create(base=base, menge=30)
        result = MovementService.store_article(incoming, self.storage.space)
        existing.refresh_from_db()
        self.assertEqual(existing.menge, 80)
        self.assertEqual(result, existing)
        self.assertFalse(Article.objects.all().filter(pk=incoming.pk).exists())

    def test_store_does_not_merge_without_flag(self):
        base = ArticleBase.objects.create(name="Hering", pType=self.article_type)
        existing = Article.objects.create(base=base, stored=self.storage.space, menge=1)
        incoming = Article.objects.create(base=base, menge=1)
        MovementService.store_article(incoming, self.storage.space)
        incoming.refresh_from_db()
        self.assertEqual(incoming.stored, self.storage.space)
        self.assertEqual(existing.menge, 1)
