from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from article.models import Article
from location.models import Location
from occasion.models import Occasion, OccasionTemplate, OccasionType, Packlist


class SeedDemoTest(TestCase):
    def _seed(self):
        call_command("seed_demo", stdout=StringIO())

    def _counts(self):
        return (
            Article.objects.count(),
            Location.objects.count(),
            OccasionType.objects.count(),
            Occasion.objects.count(),
            Packlist.objects.count(),
            OccasionTemplate.objects.count(),
        )

    def test_seed_creates_data(self):
        self._seed()
        self.assertTrue(Article.objects.exists())
        self.assertTrue(Location.objects.exists())
        self.assertTrue(OccasionType.objects.exists())
        self.assertTrue(Occasion.objects.exists())
        self.assertTrue(Packlist.objects.exists())
        self.assertTrue(OccasionTemplate.objects.exists())

    def test_seed_is_idempotent(self):
        self._seed()
        counts = self._counts()
        self._seed()
        self.assertEqual(counts, self._counts())
