from decimal import Decimal

from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from article.importer import import_articles, parse_csv, preview_import
from article.models import Article, ArticleType, Stock
from organisation.models import Organisation, Role, UserProfile
from storage.models import Storage, StorageType


class ParseCsvTest(TestCase):
    def test_comma(self):
        rows = parse_csv("name,type,menge\nHammer,tool,3\n")
        self.assertEqual(rows, [(2, {"name": "Hammer", "type": "tool", "menge": "3"})])

    def test_semicolon(self):
        rows = parse_csv("name;type;menge\nHammer;tool;3\n")
        self.assertEqual(rows[0][1]["menge"], "3")

    def test_german_headers(self):
        rows = parse_csv("Name;Typ;Menge;Lagerort;Zustand\nHammer;tool;3;Regal 1;gut\n")
        self.assertEqual(rows[0][1], {
            "name": "Hammer", "type": "tool", "menge": "3",
            "storage": "Regal 1", "zustand": "gut",
        })

    def test_blank_lines_skipped(self):
        self.assertEqual(len(parse_csv("name,type\nHammer,tool\n\n")), 1)


class ImportServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.storage_type = StorageType.objects.create(name="shelf", symbol="RE", organisation=cls.org)
        cls.storage = Storage.objects.create(name="Regal 1", typ=cls.storage_type, organisation=cls.org)

    def _rows(self, text):
        return parse_csv(text)

    def test_import_valid_row(self):
        report = import_articles(self._rows("name,type,menge\nHammer,tool,3\n"), self.org)
        self.assertEqual(report["imported"], 1)
        self.assertEqual(Article.objects.get().stocks.get().menge, Decimal("3"))

    def test_storage_by_name(self):
        import_articles(self._rows("name,type,storage\nHammer,tool,Regal 1\n"), self.org)
        self.assertEqual(Stock.objects.get().stored, self.storage.space)

    def test_unknown_type_skipped(self):
        report = import_articles(self._rows("name,type\nHammer,nope\n"), self.org)
        self.assertEqual(report["imported"], 0)
        self.assertIn("unknown type", report["errors"][0][1])

    def test_unknown_type_created(self):
        report = import_articles(self._rows("name,type\nHammer,nope\n"), self.org, {"nope": "create"})
        self.assertEqual(report["imported"], 1)
        self.assertTrue(ArticleType.objects.filter(name="nope").exists())

    def test_unknown_type_mapped(self):
        report = import_articles(
            self._rows("name,type\nHammer,nope\n"), self.org, {"nope": str(self.article_type.pk)}
        )
        self.assertEqual(report["imported"], 1)
        self.assertEqual(Article.objects.get().base.pType, self.article_type)

    def test_unknown_storage_created(self):
        report = import_articles(
            self._rows("name,type,storage\nHammer,tool,Neu\n"), self.org,
            storage_choices={"Neu": "create"},
        )
        self.assertEqual(report["imported"], 1)
        self.assertTrue(Storage.objects.filter(name="Neu").exists())

    def test_duplicate_skip(self):
        import_articles(self._rows("name,type,menge\nHammer,tool,1\n"), self.org)
        report = import_articles(self._rows("name,type,menge\nHammer,tool,5\n"), self.org, duplicates="skip")
        self.assertEqual(report["skipped"], 1)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Stock.objects.get().menge, Decimal("1"))

    def test_duplicate_update(self):
        import_articles(self._rows("name,type,menge\nHammer,tool,1\n"), self.org)
        report = import_articles(self._rows("name,type,menge\nHammer,tool,5\n"), self.org, duplicates="update")
        self.assertEqual(report["updated"], 1)
        self.assertEqual(Stock.objects.get().menge, Decimal("5"))


class PreviewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)

    def test_classification(self):
        rows = parse_csv("name,type,menge\nHammer,tool,1\nZange,nope,1\n,tool,1\n")
        preview = preview_import(rows, self.org)
        self.assertEqual(preview["total"], 3)
        self.assertEqual(preview["errors"][0][1], "missing name")
        self.assertEqual(preview["unknown_types"], ["nope"])
        self.assertFalse(Article.objects.exists())


class ImportViewTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        ArticleType.objects.create(name="tool", symbol="WZ", organisation=self.org)
        role = Role.objects.create(organisation=self.org, name="R")
        role.permissions.set(Permission.objects.filter(codename="article_create_all"))
        self.user = User.objects.create_user("u", password="pw")
        UserProfile.objects.create(user=self.user, organisation=self.org, role=role)
        self.client.login(username="u", password="pw")

    def _upload(self, text):
        return SimpleUploadedFile("a.csv", text.encode(), content_type="text/csv")

    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/import/").status_code, 200)

    def test_preview_then_confirm(self):
        response = self.client.post("/import/", {"file": self._upload("name,type,menge\nHammer,tool,2\n")})
        self.assertContains(response, "Import preview")
        response = self.client.post("/import/confirm", {"duplicates": "skip"})
        self.assertContains(response, "Imported")
        self.assertEqual(Article.objects.count(), 1)

    def test_template_download(self):
        response = self.client.get("/import/template")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_requires_permission(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/import/").status_code, 403)
