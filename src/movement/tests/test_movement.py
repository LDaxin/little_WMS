from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from space.models import Space
from storage.models import Storage, StorageType


def make_article(name, article_type, space_active):
    """Create an article the way the add-article view does (with its own Space)."""
    base = ArticleBase.objects.create(name=name, pType=article_type)
    space = Space.objects.create(prefix="a0", active=space_active)
    return Article.objects.create(base=base, space=space)


class MovementCodeInfoTest(TestCase):
    """The info returned for a scanned code (space validation)."""

    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.container_type = ArticleType.objects.create(
            name="Box", symbol="BX", article_toggle_space=True
        )
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_article_with_active_space(self):
        container = make_article("Box A", self.container_type, space_active=True)
        data = self.client.get("/movement/request/", {"code": container.code.code}).json()
        self.assertEqual(data["error"], "")
        self.assertTrue(data["storable"])
        self.assertFalse(data["storage"])
        self.assertTrue(data["space"])

    def test_article_with_inactive_space(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        data = self.client.get("/movement/request/", {"code": article.code.code}).json()
        self.assertEqual(data["error"], "")
        self.assertTrue(data["storable"])
        self.assertFalse(data["space"])

    def test_storage(self):
        data = self.client.get("/movement/request/", {"code": self.storage.code.code}).json()
        self.assertEqual(data["error"], "")
        self.assertFalse(data["storable"])
        self.assertTrue(data["storage"])
        self.assertTrue(data["space"])

    def test_unknown_code(self):
        data = self.client.get("/movement/request/", {"code": "xx123"}).json()
        self.assertNotEqual(data["error"], "")

    def test_article_without_space(self):
        base = ArticleBase.objects.create(name="Hammer", pType=self.article_type)
        article = Article.objects.create(base=base)
        data = self.client.get("/movement/request/", {"code": article.code.code}).json()
        self.assertEqual(data["error"], "")
        self.assertFalse(data["space"])

    def test_missing_code_param(self):
        data = self.client.get("/movement/request/").json()
        self.assertNotEqual(data["error"], "")


class MovementStoreTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.container_type = ArticleType.objects.create(
            name="Box", symbol="BX", article_toggle_space=True
        )
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_store_article_in_storage(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": self.storage.code.code, "articleCode1": article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertEqual(article.stored, self.storage.space)

    def test_store_article_in_container_article(self):
        container = make_article("Box A", self.container_type, space_active=True)
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": container.code.code, "articleCode1": article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertEqual(article.stored, container.space)

    def test_store_multiple_articles(self):
        first = make_article("Hammer", self.article_type, space_active=False)
        second = make_article("Zange", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {
                "storageCode": self.storage.code.code,
                "articleCode1": first.code.code,
                "articleCode2": second.code.code,
            },
        )
        self.assertEqual(response.status_code, 200)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual(first.stored, self.storage.space)
        self.assertEqual(second.stored, self.storage.space)

    def test_store_unknown_storage_code(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": "s0doesnotexist", "articleCode1": article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No storage with code")
        article.refresh_from_db()
        self.assertIsNone(article.stored)

    def test_store_unknown_prefix(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": "xx123", "articleCode1": article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown code")
        article.refresh_from_db()
        self.assertIsNone(article.stored)

    def test_store_unknown_article_code(self):
        response = self.client.post(
            "/movement/store/",
            {"storageCode": self.storage.code.code, "articleCode1": "a0doesnotexist"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No article with code")

    def test_store_into_inactive_space_rejected(self):
        inactive = Storage.objects.create(name="Regal B", typ=self.storage_type)
        inactive.space.active = False
        inactive.space.save()
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": inactive.code.code, "articleCode1": article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "not active")
        article.refresh_from_db()
        self.assertIsNone(article.stored)

    def test_store_article_into_own_space_rejected(self):
        container = make_article("Box A", self.container_type, space_active=True)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": container.code.code, "articleCode1": container.code.code},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "itself")
        container.refresh_from_db()
        self.assertIsNone(container.stored)

    def test_store_is_atomic(self):
        good = make_article("Hammer", self.article_type, space_active=False)
        bad = make_article("Box", self.container_type, space_active=True)
        response = self.client.post(
            "/movement/store/",
            {
                "storageCode": bad.code.code,
                "articleCode1": good.code.code,
                "articleCode2": bad.code.code,
            },
        )
        self.assertEqual(response.status_code, 200)
        good.refresh_from_db()
        self.assertIsNone(good.stored)


class MovementRemoveTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_remove_article(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        article.stored = self.storage.space
        article.save()
        response = self.client.post("/movement/remove/", {"articleCode1": article.code.code})
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertIsNone(article.stored)

    def test_remove_multiple_articles(self):
        first = make_article("Hammer", self.article_type, space_active=False)
        second = make_article("Zange", self.article_type, space_active=False)
        first.stored = self.storage.space
        first.save()
        second.stored = self.storage.space
        second.save()
        response = self.client.post(
            "/movement/remove/",
            {"articleCode1": first.code.code, "articleCode2": second.code.code},
        )
        self.assertEqual(response.status_code, 200)
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertIsNone(first.stored)
        self.assertIsNone(second.stored)

    def test_remove_unknown_code(self):
        response = self.client.post("/movement/remove/", {"articleCode1": "a0doesnotexist"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No article with code")
