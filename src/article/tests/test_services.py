from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, CompositionItem
from article.services import actual_quantity, composition_status, default_locations
from space.models import Space


class CompositionStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")

    def make_article(self, menge=None, stored=None):
        return Article.objects.create(base=self.base, stored=stored, menge=menge)

    def test_actual_quantity_empty(self):
        self.assertEqual(actual_quantity(self.space, self.base), 0)

    def test_actual_quantity_counts_articles(self):
        self.make_article(stored=self.space)
        self.make_article(stored=self.space)
        self.assertEqual(actual_quantity(self.space, self.base), 2)

    def test_actual_quantity_sums_menge(self):
        self.make_article(stored=self.space, menge=12)
        self.assertEqual(actual_quantity(self.space, self.base), 12)

    def test_actual_quantity_ignores_other_spaces(self):
        other = Space.objects.create(prefix="s0")
        self.make_article(stored=other)
        self.assertEqual(actual_quantity(self.space, self.base), 0)

    def test_status_underfilled(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        self.make_article(stored=self.space, menge=5)
        status = composition_status(self.space)[0]
        self.assertEqual(status["ist"], 5)
        self.assertTrue(status["underfilled"])

    def test_status_full(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        self.make_article(stored=self.space, menge=12)
        self.assertFalse(composition_status(self.space)[0]["underfilled"])

    def test_status_blank_soll_no_check(self):
        CompositionItem.objects.create(space=self.space, base=self.base)
        self.assertFalse(composition_status(self.space)[0]["underfilled"])

    def test_status_refill(self):
        CompositionItem.objects.create(space=self.space, base=self.base, mindestmenge=3)
        self.make_article(stored=self.space, menge=1)
        self.assertTrue(composition_status(self.space)[0]["refill"])

    def test_status_blank_min_no_refill(self):
        CompositionItem.objects.create(space=self.space, base=self.base)
        self.assertFalse(composition_status(self.space)[0]["refill"])


class DefaultLocationsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")

    def test_underfilled_location_is_suggested(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        self.assertEqual(default_locations(self.base), [self.space])

    def test_full_location_not_suggested(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base, stored=self.space)
        self.assertEqual(default_locations(self.base), [])

    def test_blank_soll_not_suggested(self):
        CompositionItem.objects.create(space=self.space, base=self.base)
        self.assertEqual(default_locations(self.base), [])

    def test_multiple_underfilled_locations(self):
        other = Space.objects.create(prefix="s0")
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        CompositionItem.objects.create(space=other, base=self.base, soll_menge=12)
        self.assertEqual(set(default_locations(self.base)), {self.space, other})
