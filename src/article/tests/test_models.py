from django.db import IntegrityError
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, CompositionItem
from space.models import Space


def assert_soft_delete_cycle(testcase, obj, model):
    """Characterizes the SoftDeleteObject behaviour for a concrete instance."""
    pk = obj.pk
    obj.delete()
    testcase.assertFalse(model.objects.all().filter(pk=pk).exists())
    testcase.assertTrue(model.objects.all_with_deleted().filter(pk=pk).exists())
    obj.undelete()
    testcase.assertTrue(model.objects.all().filter(pk=pk).exists())


class ArticleTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")

    def test_creation(self):
        self.assertEqual(self.article_type.symbol, "WZ")
        self.assertFalse(self.article_type.article_toggle_space)

    def test_name_is_lowercased(self):
        self.assertEqual(self.article_type.name, "werkzeug")

    def test_code_prefix(self):
        self.assertEqual(self.article_type.code.prefix, "at")

    def test_str(self):
        self.assertEqual(str(self.article_type), "werkzeug")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.article_type, ArticleType)


class ArticleBaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)

    def test_creation(self):
        self.assertEqual(self.article_base.pType, self.article_type)

    def test_code_prefix(self):
        self.assertEqual(self.article_base.code.prefix, "ab")

    def test_str(self):
        self.assertEqual(str(self.article_base), "Hammer")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.article_base, ArticleBase)

    def test_soft_delete_cascades_to_article(self):
        base = ArticleBase.objects.create(name="Zange", pType=self.article_type)
        article = Article.objects.create(base=base)
        base.delete()
        self.assertFalse(Article.objects.all().filter(pk=article.pk).exists())
        self.assertTrue(Article.objects.all_with_deleted().filter(pk=article.pk).exists())


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

    def test_creation(self):
        self.assertEqual(self.article.base, self.article_base)

    def test_code_prefix(self):
        self.assertEqual(self.article.code.prefix, "a0")

    def test_optional_fields_default_null(self):
        self.assertIsNone(self.article.stored)
        self.assertIsNone(self.article.space)
        self.assertIsNone(self.article.amount)

    def test_str(self):
        self.assertEqual(str(self.article), "Hammer " + self.article.code.code)

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.article, Article)


class ArticleGlobalFieldsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

    def test_article_defaults(self):
        self.assertEqual(self.article.zustand, "gut")
        self.assertFalse(self.article.ist_verbrauchsartikel)
        self.assertIsNone(self.article.menge)
        self.assertIsNone(self.article.anschaffungswert)
        self.assertEqual(self.article.notiz, "")

    def test_article_base_catalog_defaults(self):
        self.assertEqual(self.article_base.attributes, {})
        self.assertIsNone(self.article_base.outer_length_mm)
        self.assertIsNone(self.article_base.size_class)

    def test_article_type_allow_merge_split_default(self):
        self.assertFalse(self.article_type.allow_merge_split)


class CompositionItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")

    def test_creation(self):
        item = CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        self.assertEqual(item.soll_menge, 12)
        self.assertIsNone(item.mindestmenge)

    def test_unique_together(self):
        CompositionItem.objects.create(space=self.space, base=self.base)
        with self.assertRaises(IntegrityError):
            CompositionItem.objects.create(space=self.space, base=self.base)
