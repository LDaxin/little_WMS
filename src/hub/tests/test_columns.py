from django.test import TestCase

from article.models import Article
from hub import columns
from storage.models import Storage


class ColumnRegistryTest(TestCase):
    def test_unique_keys(self):
        for list_type in columns.LIST_TYPES:
            keys = [c.key for c in columns.columns(list_type)]
            self.assertEqual(len(keys), len(set(keys)), list_type)

    def test_defaults_are_available(self):
        for list_type in columns.LIST_TYPES:
            available = {c.key for c in columns.columns(list_type)}
            for c in columns.default_columns(list_type):
                self.assertIn(c.key, available)

    def test_column_lookup(self):
        self.assertEqual(columns.column("article", "name").path, "base__name")
        self.assertIsNone(columns.column("article", "nope"))

    def test_sort_path(self):
        self.assertEqual(columns.sort_path("article", "name"), "base__name")
        self.assertIsNone(columns.sort_path("article", "location"))
        self.assertIsNone(columns.sort_path("article", "nope"))

    def test_resolve(self):
        class Obj:
            pass

        a = Obj()
        a.b = Obj()
        a.b.c = 5
        self.assertEqual(columns.resolve(a, "b__c"), 5)
        self.assertIsNone(columns.resolve(a, "b__x"))

    def test_sortable_paths_are_valid(self):
        for c in columns.columns("article"):
            if c.sortable:
                Article.objects.order_by(c.path).first()
        for c in columns.columns("storage"):
            if c.sortable:
                Storage.objects.order_by(c.path).first()
