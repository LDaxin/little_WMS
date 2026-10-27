from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from space.models import Space
from space.services import can_store, max_storage_depth


def make_article(name, article_type):
    base = ArticleBase.objects.create(name=name, pType=article_type)
    space = Space.objects.create(prefix="a0", active=True)
    return Article.objects.create(base=base, space=space)


class CanStoreTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")

    def test_ok(self):
        container = make_article("Box", self.article_type)
        article = make_article("Hammer", self.article_type)
        ok, reason = can_store(article.space, container.space, 7)
        self.assertTrue(ok)
        self.assertEqual(reason, "")

    def test_self_storage(self):
        article = make_article("Hammer", self.article_type)
        ok, reason = can_store(article.space, article.space, 7)
        self.assertFalse(ok)
        self.assertIn("itself", reason)

    def test_cycle(self):
        # A is stored in B's space and B in A's space -> cycle.
        a = make_article("A", self.article_type)
        b = make_article("B", self.article_type)
        Stock.objects.create(article=a, stored=b.space, menge=1)
        Stock.objects.create(article=b, stored=a.space, menge=1)
        ok, reason = can_store(a.space, b.space, 7)
        self.assertFalse(ok)
        self.assertIn("Cycle", reason)

    def test_depth(self):
        # A chain of nested containers deeper than max_depth.
        prev = None
        for i in range(8):
            article = make_article("N%d" % i, self.article_type)
            if prev is not None:
                Stock.objects.create(article=article, stored=prev.space, menge=1)
            prev = article
        ok, reason = can_store(None, prev.space, 3)
        self.assertFalse(ok)
        self.assertIn("depth", reason)

    def test_max_storage_depth_default(self):
        self.assertEqual(max_storage_depth(), 7)
