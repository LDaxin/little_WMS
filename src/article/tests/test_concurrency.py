from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType


class OptimisticLockingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def _update(self, version):
        return self.client.post("/article/werkzeug/%s/update" % self.article.pk, {
            "base-name": "Hammer XL",
            "article-amount": "3",
            "article-stored": "",
            "article-zustand": "gut",
            "version": version,
        })

    def test_save_with_current_version(self):
        self._update(str(self.article.version))
        self.article.refresh_from_db()
        self.assertEqual(self.article.base.name, "Hammer XL")
        self.assertEqual(self.article.version, 1)

    def test_save_with_stale_version(self):
        response = self._update("999")
        self.article.refresh_from_db()
        self.assertNotEqual(self.article.base.name, "Hammer XL")
        self.assertContains(response, "changed by someone else")
