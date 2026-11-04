from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType

from hub.tests.html import ids_inside


class ListControlsMarkupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="tent", symbol="TZ")
        cls.article = Article.objects.create(
            base=ArticleBase.objects.create(name="Jurte", pType=cls.article_type)
        )

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_search_row_and_control_bar_are_wrapped(self):
        html = self.client.get("/article/tent/").content.decode()
        inside = ids_inside(html, "listControls")
        self.assertIn("listSearchRow", inside)
        self.assertIn("listControlBar", inside)

    def test_advanced_trigger_in_the_search_row(self):
        html = self.client.get("/article/tent/").content.decode()
        self.assertIn("qbToggleButton", ids_inside(html, "listSearchRow"))

    def test_scanner_container_is_outside_the_controls(self):
        html = self.client.get("/article/tent/").content.decode()
        self.assertNotIn("scannerDivarticleSearchtent", ids_inside(html, "listControls"))
