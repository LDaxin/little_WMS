import io
from decimal import Decimal

from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.importer import import_articles
from article.models import Article, ArticleType, Stock
from organisation.models import Organisation, Role, UserProfile
from storage.models import Storage, StorageType


class ImportServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.storage_type = StorageType.objects.create(name="shelf", symbol="RE", organisation=cls.org)
        cls.storage = Storage.objects.create(name="Regal 1", typ=cls.storage_type, organisation=cls.org)

    def _csv(self, text):
        return io.StringIO(text)

    def test_import_valid_row(self):
        report = import_articles(self._csv("name,type,menge,storage,zustand\nHammer,tool,3,,\n"), self.org)
        self.assertEqual(report["imported"], 1)
        self.assertEqual(report["errors"], [])
        article = Article.objects.get()
        self.assertEqual(article.base.name, "Hammer")
        self.assertEqual(article.stocks.get().menge, Decimal("3"))

    def test_storage_by_name(self):
        import_articles(self._csv("name,type,menge,storage\nHammer,tool,1,Regal 1\n"), self.org)
        self.assertEqual(Stock.objects.get().stored, self.storage.space)

    def test_unknown_type(self):
        report = import_articles(self._csv("name,type\nHammer,nope\n"), self.org)
        self.assertEqual(report["imported"], 0)
        self.assertEqual(report["errors"][0][1], "unknown type: nope")
        self.assertFalse(Article.objects.exists())

    def test_unknown_storage(self):
        report = import_articles(self._csv("name,type,storage\nHammer,tool,Nope\n"), self.org)
        self.assertEqual(report["imported"], 0)
        self.assertIn("unknown storage", report["errors"][0][1])
        self.assertFalse(Article.objects.exists())

    def test_missing_name(self):
        report = import_articles(self._csv("name,type\n,tool\n"), self.org)
        self.assertEqual(report["errors"][0][1], "missing name")


class ImportViewTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        role = Role.objects.create(organisation=self.org, name="R")
        role.permissions.set(Permission.objects.filter(codename="article_create_all"))
        self.user = User.objects.create_user("u", password="pw")
        UserProfile.objects.create(user=self.user, organisation=self.org, role=role)
        self.client.login(username="u", password="pw")

    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/import/").status_code, 200)

    def test_template_download(self):
        response = self.client.get("/import/template")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_requires_permission(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/import/").status_code, 403)
