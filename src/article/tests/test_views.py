from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from storage.models import Storage, StorageType


class ArticleViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_pages_return_200(self):
        urls = [
            "/article/werkzeug/",
            "/article/werkzeug/add/modal",
            "/article/werkzeug/del/modal",
            f"/article/werkzeug/{self.article.pk}",
            f"/article/werkzeug/{self.article.pk}/i",
            "/article/werkzeug/search?search=",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/article/werkzeug/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_detail_shows_canonical_link(self):
        response = self.client.get(f"/article/werkzeug/{self.article.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.code.code)
        self.assertContains(response, "/a/" + self.article.code.code)

    def test_add_article(self):
        response = self.client.post(
            "/article/werkzeug/add",
            {
                "base-name": "Zange",
                "article-amount": "",
                "article-stored": "",
                "article-code": "",
                "article-zustand": "gut",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ArticleBase.objects.filter(name="Zange").exists())

    def test_add_article_with_custom_fields(self):
        self.article_type.custom_fields_schema = {
            "fields": [
                {"name": "farbe", "type": "text", "level": "base"},
                {"name": "seriennummer", "type": "text", "level": "article"},
            ]
        }
        self.article_type.save()
        response = self.client.post(
            "/article/werkzeug/add",
            {
                "base-name": "Zange",
                "base-farbe": "rot",
                "article-seriennummer": "SN-9",
                "article-amount": "",
                "article-stored": "",
                "article-code": "",
                "article-zustand": "gut",
            },
        )
        self.assertEqual(response.status_code, 200)
        base = ArticleBase.objects.get(name="Zange")
        self.assertEqual(base.attributes, {"farbe": "rot"})
        self.assertEqual(base.article_set.first().attributes, {"seriennummer": "SN-9"})

    def test_update_article(self):
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/update",
            {
                "base-name": "Hammer XL",
                "article-amount": "3",
                "article-stored": "",
                "article-zustand": "gut",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.article_base.refresh_from_db()
        self.assertEqual(self.article_base.name, "Hammer XL")

    def test_delete_article(self):
        response = self.client.post(
            "/article/werkzeug/del", {f"_{self.article.pk}": str(self.article.pk)}
        )
        self.assertEqual(response.status_code, 200)
        # SoftDeleteManager.filter(pk=...) intentionally includes soft-deleted
        # rows, so the filtered queryset is used here (see softdelete/models.py).
        self.assertFalse(Article.objects.all().filter(pk=self.article.pk).exists())

    def test_export_articles(self):
        response = self.client.post(
            "/article/werkzeug/export", {f"_{self.article.pk}": str(self.article.pk)}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=iso-8859-1")


class ArticleStoreRemoveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_store_article(self):
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/store",
            {"code": self.storage.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.stored, self.storage.space)

    def test_store_article_unknown_code(self):
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/store",
            {"code": "xx123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown code")
        self.article.refresh_from_db()
        self.assertIsNone(self.article.stored)

    def test_remove_article(self):
        self.article.stored = self.storage.space
        self.article.save()
        response = self.client.post(f"/article/werkzeug/{self.article.pk}/remove")
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertIsNone(self.article.stored)

    def test_add_article_with_stored_code(self):
        response = self.client.post(
            "/article/werkzeug/add",
            {
                "base-name": "Zange",
                "article-amount": "",
                "article-stored": self.storage.code.code,
                "article-code": "",
                "article-zustand": "gut",
            },
        )
        self.assertEqual(response.status_code, 200)
        article = Article.objects.get(base__name="Zange")
        self.assertEqual(article.stored, self.storage.space)

    def test_add_article_with_unknown_stored_code(self):
        response = self.client.post(
            "/article/werkzeug/add",
            {
                "base-name": "Zange",
                "article-amount": "",
                "article-stored": "xx123",
                "article-code": "",
                "article-zustand": "gut",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown code")
        self.assertFalse(Article.objects.filter(base__name="Zange").exists())
