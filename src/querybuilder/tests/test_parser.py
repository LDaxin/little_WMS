from django.db.models import Q
from django.test import TestCase

from querybuilder.services import ARTICLE_FIELDS, QueryError, parse, parse_json


class ParserTest(TestCase):
    def test_and(self):
        q = parse({"type": "AND", "conditions": [
            {"field": "base__name", "op": "eq", "value": "Tent"},
            {"field": "zustand", "op": "eq", "value": "gut"},
        ]}, ARTICLE_FIELDS)
        self.assertEqual(q, Q(base__name__exact="Tent") & Q(zustand__exact="gut"))

    def test_nested_or(self):
        q = parse({"type": "AND", "conditions": [
            {"field": "base__name", "op": "eq", "value": "Tent"},
            {"type": "OR", "conditions": [
                {"field": "gewicht_gramm", "op": "gt", "value": 5000},
                {"field": "tags__name", "op": "contains", "value": "summer"},
            ]},
        ]}, ARTICLE_FIELDS)
        self.assertEqual(
            q,
            Q(base__name__exact="Tent")
            & (Q(gewicht_gramm__gt=5000) | Q(tags__name__icontains="summer")),
        )

    def test_not_group(self):
        q = parse({"type": "AND", "negate": True, "conditions": [
            {"field": "zustand", "op": "eq", "value": "kaputt"},
        ]}, ARTICLE_FIELDS)
        self.assertEqual(q, ~Q(zustand__exact="kaputt"))

    def test_negated_operator(self):
        q = parse({"field": "zustand", "op": "ne", "value": "kaputt"}, ARTICLE_FIELDS)
        self.assertEqual(q, ~Q(zustand__exact="kaputt"))

    def test_unknown_field(self):
        with self.assertRaises(QueryError):
            parse({"field": "nope", "op": "eq", "value": "x"}, ARTICLE_FIELDS)

    def test_disallowed_operator(self):
        with self.assertRaises(QueryError):
            parse({"field": "base__name", "op": "gt", "value": "x"}, ARTICLE_FIELDS)

    def test_parse_json(self):
        q = parse_json('{"field": "base__name", "op": "contains", "value": "Ham"}', ARTICLE_FIELDS)
        self.assertEqual(q, Q(base__name__icontains="Ham"))

    def test_parse_json_invalid(self):
        with self.assertRaises(QueryError):
            parse_json("{not json", ARTICLE_FIELDS)
