from django.core.exceptions import ValidationError
from django.test import TestCase

from article.models import ArticleType


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


class ArticleTypeSchemaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(
            name="Zelt", symbol="TZ", custom_fields_schema=SCHEMA
        )

    def test_defaults(self):
        plain = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        self.assertEqual(plain.field_config, {})
        self.assertEqual(plain.custom_fields_schema, {})

    def test_fields_for_level(self):
        self.assertEqual(
            [f["name"] for f in self.article_type.fields_for_level("base")],
            ["farbe", "personenzahl", "saison"],
        )
        self.assertEqual(
            [f["name"] for f in self.article_type.fields_for_level("article")],
            ["seriennummer"],
        )

    def test_valid_attributes(self):
        self.article_type.validate_attributes(
            {"farbe": "rot", "personenzahl": 8, "saison": "4-Season"}
        )

    def test_optional_fields_may_be_missing(self):
        self.article_type.validate_attributes({"personenzahl": 8})

    def test_required_missing(self):
        with self.assertRaises(ValidationError) as ctx:
            self.article_type.validate_attributes({"farbe": "rot"})
        self.assertIn("personenzahl", ctx.exception.message_dict)

    def test_wrong_type(self):
        with self.assertRaises(ValidationError) as ctx:
            self.article_type.validate_attributes({"personenzahl": "acht"})
        self.assertIn("personenzahl", ctx.exception.message_dict)

    def test_min_max(self):
        with self.assertRaises(ValidationError) as ctx:
            self.article_type.validate_attributes({"personenzahl": 30})
        self.assertIn("personenzahl", ctx.exception.message_dict)

    def test_invalid_choice(self):
        with self.assertRaises(ValidationError) as ctx:
            self.article_type.validate_attributes(
                {"personenzahl": 8, "saison": "Winter"}
            )
        self.assertIn("saison", ctx.exception.message_dict)
