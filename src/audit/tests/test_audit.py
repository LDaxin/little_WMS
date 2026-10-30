from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from audit.models import AuditLog
from audit.services import log
from storage.models import Storage, StorageType


class AuditServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=cls.base)

    def test_log_creates_entry(self):
        entry = log("created", self.article, changes={"name": "Hammer"})
        self.assertEqual(entry.action, "created")
        self.assertEqual(entry.content_object, self.article)
        self.assertEqual(entry.changes, {"name": "Hammer"})
        self.assertEqual(AuditLog.objects.count(), 1)


class ArticleAuditTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=cls.base)
        storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=storage_type)

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def actions(self):
        return set(AuditLog.objects.values_list("action", flat=True))

    def test_add_logs_created(self):
        self.client.post(
            "/article/werkzeug/add",
            {"base-name": "Zange", "article-amount": "", "article-stored": "",
             "article-code": "", "article-zustand": "gut"},
        )
        self.assertIn("created", self.actions())

    def test_update_logs_updated(self):
        self.client.post(
            f"/article/werkzeug/{self.article.pk}/update",
            {"base-name": "Hammer", "article-amount": "", "article-stored": "",
             "article-zustand": "defekt"},
        )
        entry = AuditLog.objects.filter(action="updated").first()
        self.assertIsNotNone(entry)
        self.assertIn("zustand", entry.changes)

    def test_store_logs_moved(self):
        self.client.post(
            f"/article/werkzeug/{self.article.pk}/store",
            {"code": self.storage.code.code},
        )
        self.assertIn("moved", self.actions())

    def test_delete_logs_deleted(self):
        self.client.post(
            "/article/werkzeug/del", {f"_{self.article.pk}": str(self.article.pk)}
        )
        self.assertIn("deleted", self.actions())

    def test_detail_shows_timeline(self):
        log("created", self.article)
        response = self.client.get(f"/article/werkzeug/{self.article.pk}")
        self.assertContains(response, "History")
