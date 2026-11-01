import json
import os
import tempfile

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from organisation.export import export_organisation, import_organisation
from organisation.models import Organisation
from storage.models import Storage, StorageType


class ExportImportTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        self.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=self.org)
        self.base = ArticleBase.objects.create(name="Hammer", pType=self.article_type, organisation=self.org)
        self.article = Article.objects.create(base=self.base, organisation=self.org)
        self.storage_type = StorageType.objects.create(name="shelf", symbol="RE", organisation=self.org)
        self.storage = Storage.objects.create(name="Regal 1", typ=self.storage_type, organisation=self.org)
        Stock.objects.create(article=self.article, stored=self.storage.space, menge=3)

    def test_export_only_that_org(self):
        other = Organisation.objects.create(name="B", slug="b")
        ArticleType.objects.create(name="other", symbol="XX", organisation=other)
        data = export_organisation(self.org)
        names = [
            o["fields"].get("name")
            for o in data["objects"]
            if o["model"] == "article.articletype"
        ]
        self.assertEqual(names, ["tool"])

    def test_import_creates_new_org(self):
        data = export_organisation(self.org)
        new_org = import_organisation(data, name="Copy")
        self.assertNotEqual(new_org.pk, self.org.pk)
        self.assertTrue(ArticleType.objects.filter(organisation=new_org, name="tool").exists())
        self.assertTrue(Article.objects.filter(organisation=new_org).exists())

    def test_references_remapped(self):
        data = export_organisation(self.org)
        new_org = import_organisation(data, name="Copy")
        article = Article.objects.get(organisation=new_org)
        self.assertEqual(article.base.pType.organisation, new_org)
        stock = Stock.objects.get(article=article)
        self.assertEqual(stock.stored.organisation, new_org)

    def test_self_reference(self):
        child = Storage.objects.create(name="Fach X", typ=self.storage_type, organisation=self.org)
        parent = Storage.objects.create(name="Regal X", typ=self.storage_type, organisation=self.org)
        child.parent = parent
        child.save()
        data = export_organisation(self.org)
        new_org = import_organisation(data, name="Copy")
        new_child = Storage.objects.get(organisation=new_org, name="Fach X")
        self.assertEqual(new_child.parent.name, "Regal X")


class ExportCommandTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        ArticleType.objects.create(name="tool", symbol="WZ", organisation=self.org)

    def test_export_and_import_commands(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            call_command("export_organisation", "a", path)
            self.assertTrue(os.path.getsize(path) > 0)
            call_command("import_organisation", path, "--name", "Copy")
            self.assertTrue(Organisation.objects.filter(name="Copy").exists())
        finally:
            os.remove(path)


class ExportViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("root", "root@example.com", "pw")
        self.client.login(username="root", password="pw")

    def test_download(self):
        response = self.client.get("/server-settings/export/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])

    def test_requires_superuser(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/server-settings/export/").status_code, 403)
