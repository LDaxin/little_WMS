from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from occasion.models import Occasion, OccasionType, Packlist
from planning.models import CalendarEntry


class ArticleMiniCalendarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.occ_type = OccasionType.objects.create(name="Camp")

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")
        self.article = Article.objects.create(base=self.base)

    def _detail(self):
        return self.client.get("/article/werkzeug/%s?calendar_view=list" % self.article.pk)

    def test_occasion_term(self):
        entry = CalendarEntry.objects.create(title="Sommerlager", start_date="2026-07-01")
        occasion = Occasion.objects.create(calendar_entry=entry, occasion_type=self.occ_type)
        Packlist.objects.create(occasion=occasion, article=self.article, quantity=1)
        response = self._detail()
        self.assertContains(response, "Occasion: Sommerlager")
        self.assertContains(response, "/occasions/%s/" % occasion.pk)

    def test_expiry_term(self):
        self.article.ablaufdatum = "2026-12-31"
        self.article.save()
        response = self._detail()
        self.assertContains(response, "Expires")
        self.assertContains(response, "2026-12-31")

    def test_empty_state(self):
        self.assertContains(self._detail(), "No terms")
