from django.core.management import call_command
from django.test import TestCase

from article.models import Article, Stock


class SeedArticlesTest(TestCase):
    def test_creates_articles_with_stocks(self):
        call_command("seed_articles", count=3)
        self.assertEqual(Article.objects.count(), 3)
        self.assertEqual(Stock.objects.count(), 3)

    def test_idempotent(self):
        call_command("seed_articles", count=3)
        call_command("seed_articles", count=3)
        self.assertEqual(Article.objects.count(), 3)
