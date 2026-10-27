from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, CompositionItem, Stock
from article.services import actual_quantity, allocation, composition_status, consume, default_locations, location_minimum_sum
from space.models import Space


class CompositionStatusTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")

    def make_article(self, menge=1, stored=None):
        article = Article.objects.create(base=self.base)
        Stock.objects.create(article=article, stored=stored, menge=menge)
        return article

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
        article = Article.objects.create(base=self.base)
        Stock.objects.create(article=article, stored=self.space, menge=1)
        self.assertEqual(default_locations(self.base), [])

    def test_blank_soll_not_suggested(self):
        CompositionItem.objects.create(space=self.space, base=self.base)
        self.assertEqual(default_locations(self.base), [])

    def test_multiple_underfilled_locations(self):
        other = Space.objects.create(prefix="s0")
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        CompositionItem.objects.create(space=other, base=self.base, soll_menge=12)
        self.assertEqual(set(default_locations(self.base)), {self.space, other})


class MinimumTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")
        cls.other = Space.objects.create(prefix="s0")

    def test_location_minimum_sum(self):
        CompositionItem.objects.create(space=self.space, base=self.base, mindestmenge=3)
        CompositionItem.objects.create(space=self.other, base=self.base, mindestmenge=4)
        self.assertEqual(location_minimum_sum(self.base), 7)

    def test_status_reports_global_and_min_sum(self):
        self.base.mindestbestand = 5
        self.base.save()
        CompositionItem.objects.create(space=self.space, base=self.base, mindestmenge=3)
        row = composition_status(self.space)[0]
        self.assertEqual(row["global"], 5)
        self.assertEqual(row["min_sum"], 3)


class AllocationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")
        cls.other = Space.objects.create(prefix="s0")

    def test_not_over_when_enough_articles(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=1)
        CompositionItem.objects.create(space=self.other, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base)
        Article.objects.create(base=self.base)
        self.assertFalse(allocation(self.base)["over"])

    def test_over_when_too_few_articles(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=1)
        CompositionItem.objects.create(space=self.other, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base)
        alloc = allocation(self.base)
        self.assertTrue(alloc["over"])
        self.assertEqual(alloc["soll"], 2)
        self.assertEqual(alloc["available"], 1)

    def test_status_over_flag(self):
        CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=1)
        CompositionItem.objects.create(space=self.other, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base)
        self.assertTrue(composition_status(self.space)[0]["over"])


class ConsumeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(
            name="Perlen", symbol="PR", allow_merge_split=True
        )
        cls.base = ArticleBase.objects.create(name="Bügelperle", pType=cls.article_type)

    def make(self, menge):
        article = Article.objects.create(base=self.base)
        Stock.objects.create(article=article, stored=None, menge=menge)
        return article

    def test_consume_decrements(self):
        article = self.make(5)
        consume(article, 2)
        self.assertEqual(article.stocks.get(stored=None).menge, 3)

    def test_consume_to_zero_deletes(self):
        article = self.make(2)
        consume(article, 2)
        self.assertFalse(Article.objects.all().filter(pk=article.pk).exists())
        self.assertTrue(Article.objects.all_with_deleted().filter(pk=article.pk).exists())

    def test_consume_below_zero_deletes(self):
        article = self.make(1)
        consume(article, 5)
        self.assertFalse(Article.objects.all().filter(pk=article.pk).exists())
