from django.test import TestCase

from article.forms import FormArticle, FormArticleBase
from article.models import Article, ArticleBase, ArticleType


SCHEMA = {
    "fields": [
        {"name": "farbe", "type": "text", "level": "base"},
        {
            "name": "personenzahl",
            "type": "integer",
            "required": True,
            "min": 1,
            "max": 20,
            "level": "base",
        },
        {
            "name": "saison",
            "type": "choice",
            "options": ["3-Season", "4-Season"],
            "level": "base",
        },
        {"name": "seriennummer", "type": "text", "level": "article"},
    ]
}

FIELD_CONFIG = {
    "anschaffungswert": {"visible": False},
    "notiz": {"required": True},
}


class ArticleFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(
            name="Zelt",
            symbol="TZ",
            field_config=FIELD_CONFIG,
            custom_fields_schema=SCHEMA,
        )
        cls.article_base = ArticleBase.objects.create(name="Jurte", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

    def test_field_config_hides_field(self):
        form = FormArticle(article_type=self.article_type)
        self.assertNotIn("anschaffungswert", form.fields)

    def test_field_config_marks_required(self):
        form = FormArticle(article_type=self.article_type)
        self.assertTrue(form.fields["notiz"].required)

    def test_without_article_type_all_fields_visible(self):
        form = FormArticle()
        self.assertIn("anschaffungswert", form.fields)
        self.assertFalse(form.fields["notiz"].required)

    def test_base_custom_fields_rendered(self):
        form = FormArticleBase(article_type=self.article_type)
        self.assertIn("farbe", form.fields)
        self.assertIn("personenzahl", form.fields)
        self.assertIn("saison", form.fields)
        self.assertNotIn("seriennummer", form.fields)

    def test_article_custom_fields_rendered(self):
        form = FormArticle(article_type=self.article_type)
        self.assertIn("seriennummer", form.fields)
        self.assertNotIn("farbe", form.fields)

    def test_custom_field_required(self):
        form = FormArticleBase(article_type=self.article_type)
        self.assertTrue(form.fields["personenzahl"].required)
        self.assertFalse(form.fields["farbe"].required)

    def test_custom_field_choice_options(self):
        form = FormArticleBase(article_type=self.article_type)
        self.assertEqual(
            [c[0] for c in form.fields["saison"].choices],
            ["3-Season", "4-Season"],
        )

    def test_base_values_saved_to_attributes(self):
        form = FormArticleBase(
            {"name": "Jurte", "farbe": "rot", "personenzahl": "8", "saison": "4-Season"},
            instance=self.article_base,
            article_type=self.article_type,
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.article_base.refresh_from_db()
        self.assertEqual(
            self.article_base.attributes,
            {"farbe": "rot", "personenzahl": 8, "saison": "4-Season"},
        )

    def test_article_values_saved_to_attributes(self):
        form = FormArticle(
            {"seriennummer": "SN-1", "zustand": "gut", "notiz": "x"},
            instance=self.article,
            article_type=self.article_type,
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.article.refresh_from_db()
        self.assertEqual(self.article.attributes, {"seriennummer": "SN-1"})

    def test_initial_values_loaded(self):
        self.article_base.attributes = {"farbe": "blau", "personenzahl": 4}
        self.article_base.save()
        form = FormArticleBase(instance=self.article_base, article_type=self.article_type)
        self.assertEqual(form.initial["farbe"], "blau")
        self.assertEqual(form.initial["personenzahl"], 4)

    def test_cleared_value_removed(self):
        self.article_base.attributes = {"farbe": "blau"}
        self.article_base.save()
        form = FormArticleBase(
            {"name": "Jurte", "farbe": "", "personenzahl": "8"},
            instance=self.article_base,
            article_type=self.article_type,
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.article_base.refresh_from_db()
        self.assertNotIn("farbe", self.article_base.attributes)


class MergeSplitFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.no_merge = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.merge = ArticleType.objects.create(name="Perlen", symbol="PR", allow_merge_split=True)
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.no_merge)

    def test_menge_hidden_without_merge_split(self):
        self.assertNotIn("menge", FormArticle(article_type=self.no_merge).fields)

    def test_menge_visible_with_merge_split(self):
        self.assertIn("menge", FormArticle(article_type=self.merge).fields)
