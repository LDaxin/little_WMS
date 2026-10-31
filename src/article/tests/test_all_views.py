from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType


class AllArticlesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="tent", symbol="TZ")
        base = ArticleBase.objects.create(name="Jurte", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_articles_all(self):
        self.assertEqual(self.client.get("/article/").status_code, 200)

    def test_search_all(self):
        response = self.client.get("/article/search", {"search": "Jurte"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jurte")
