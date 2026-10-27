from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, CompositionItem
from space.models import Space
from storage.models import Storage, StorageType
from tag.models import Tag


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


class ArticleStoreToDefaultTest(TestCase):
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

    def test_store_to_default(self):
        CompositionItem.objects.create(space=self.storage.space, base=self.article_base, soll_menge=1)
        response = self.client.post(f"/article/werkzeug/{self.article.pk}/store-default")
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.stored, self.storage.space)

    def test_store_to_default_redirects(self):
        CompositionItem.objects.create(space=self.storage.space, base=self.article_base, soll_menge=1)
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/store-default",
            {"next": "/where/?q=" + self.article.code.code},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/where/?q=" + self.article.code.code)

    def test_store_to_default_without_composition(self):
        response = self.client.post(f"/article/werkzeug/{self.article.pk}/store-default")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No default location")
        self.article.refresh_from_db()
        self.assertIsNone(self.article.stored)


class ArticleTagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)
        cls.tag = Tag.objects.create(name="summer", color="#ff0000")

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_add_tag(self):
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/tags/add", {"tag": "summer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tag, self.article.tags.all())

    def test_add_unknown_tag(self):
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/tags/add", {"tag": "nope"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tag named")
        self.assertEqual(self.article.tags.count(), 0)

    def test_remove_tag(self):
        self.article.tags.add(self.tag)
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/tags/remove/{self.tag.pk}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.article.tags.count(), 0)


class CompositionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="s0")

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_add_composition_item(self):
        for _ in range(12):
            Article.objects.create(base=self.base)
        response = self.client.post(
            f"/composition/{self.space.pk}/add",
            {"base": "Hering", "soll": "12", "min": "3"},
        )
        self.assertEqual(response.status_code, 200)
        item = CompositionItem.objects.get(space=self.space, base=self.base)
        self.assertEqual(item.soll_menge, 12)
        self.assertEqual(item.mindestmenge, 3)

    def test_add_composition_item_blank_values(self):
        response = self.client.post(
            f"/composition/{self.space.pk}/add",
            {"base": "Hering", "soll": "", "min": ""},
        )
        self.assertEqual(response.status_code, 200)
        item = CompositionItem.objects.get(space=self.space, base=self.base)
        self.assertIsNone(item.soll_menge)
        self.assertIsNone(item.mindestmenge)

    def test_add_composition_item_unknown_base(self):
        response = self.client.post(
            f"/composition/{self.space.pk}/add",
            {"base": "nope", "soll": "1", "min": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No article base named")
        self.assertEqual(self.space.composition.count(), 0)

    def test_remove_composition_item(self):
        item = CompositionItem.objects.create(space=self.space, base=self.base, soll_menge=12)
        response = self.client.post(f"/composition/{self.space.pk}/remove/{item.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.space.composition.count(), 0)

    def test_add_composition_item_over_allocated_warns(self):
        other = Space.objects.create(prefix="s0")
        CompositionItem.objects.create(space=other, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base)
        response = self.client.post(
            f"/composition/{self.space.pk}/add",
            {"base": "Hering", "soll": "1", "min": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Only 1 Hering available")
        self.assertEqual(self.space.composition.count(), 0)

    def test_add_composition_item_over_allocated_forced(self):
        other = Space.objects.create(prefix="s0")
        CompositionItem.objects.create(space=other, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base)
        response = self.client.post(
            f"/composition/{self.space.pk}/add",
            {"base": "Hering", "soll": "1", "min": "", "force": "1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.space.composition.count(), 1)


class CompositionWarningTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.base = ArticleBase.objects.create(name="Hering", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.base)
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_store_into_full_location_warns(self):
        CompositionItem.objects.create(space=self.storage.space, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base, stored=self.storage.space)
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/store",
            {"code": self.storage.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Already enough")
        self.article.refresh_from_db()
        self.assertIsNone(self.article.stored)

    def test_store_into_full_location_forced(self):
        CompositionItem.objects.create(space=self.storage.space, base=self.base, soll_menge=1)
        Article.objects.create(base=self.base, stored=self.storage.space)
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/store",
            {"code": self.storage.code.code, "force": "1"},
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.stored, self.storage.space)

    def test_store_into_underfilled_location_no_warning(self):
        CompositionItem.objects.create(space=self.storage.space, base=self.base, soll_menge=12)
        response = self.client.post(
            f"/article/werkzeug/{self.article.pk}/store",
            {"code": self.storage.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.stored, self.storage.space)


class CompositionRenderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(
            name="Box", symbol="BX", article_toggle_space=True
        )
        cls.article_base = ArticleBase.objects.create(name="Box A", pType=cls.article_type)
        cls.space = Space.objects.create(prefix="a0", active=True)
        cls.article = Article.objects.create(base=cls.article_base, space=cls.space)
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_container_detail_shows_composition(self):
        response = self.client.get(f"/article/box/{self.article.pk}")
        self.assertContains(response, "Composition")

    def test_storage_detail_shows_composition(self):
        response = self.client.get(f"/storage/regal/{self.storage.pk}")
        self.assertContains(response, "Composition")


class ArticleConsumeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(
            name="Perlen", symbol="PR", allow_merge_split=True
        )
        cls.article_base = ArticleBase.objects.create(name="Bügelperle", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base, menge=5)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_mergeable_article_shows_amount_input(self):
        response = self.client.get(f"/article/perlen/{self.article.pk}")
        self.assertContains(response, 'name="amount"')

    def test_update_article_menge_zero_deletes(self):
        response = self.client.post(
            f"/article/perlen/{self.article.pk}/update",
            {
                "base-name": "Bügelperle",
                "article-amount": "",
                "article-stored": "",
                "article-zustand": "gut",
                "article-menge": "0",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.all().filter(pk=self.article.pk).exists())

    def test_update_article_menge_kept(self):
        response = self.client.post(
            f"/article/perlen/{self.article.pk}/update",
            {
                "base-name": "Bügelperle",
                "article-amount": "",
                "article-stored": "",
                "article-zustand": "gut",
                "article-menge": "3",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.menge, 3)
