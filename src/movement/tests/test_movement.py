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
    """Characterizes the "space validation" info returned for a scanned code."""

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

    def test_article_without_space_raises(self):
        # Characterization: an article without a Space makes movementCodeInfo
        # raise AttributeError (HTTP 500).
        base = ArticleBase.objects.create(name="Hammer", pType=self.article_type)
        article = Article.objects.create(base=base)
        with self.assertRaises(AttributeError), self.assertLogs("django.request", level="ERROR"):
            self.client.get("/movement/request/", {"code": article.code.code})

    def test_missing_code_param_raises(self):
        # Characterization: `request.GET['code']` without `.get()` -> KeyError.
        with self.assertRaises(KeyError), self.assertLogs("django.request", level="ERROR"):
            self.client.get("/movement/request/")


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

    def test_store_unknown_storage_code_raises(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        with self.assertRaises(Storage.DoesNotExist), self.assertLogs(
            "django.request", level="ERROR"
        ):
            self.client.post(
                "/movement/store/",
                {"storageCode": "s0doesnotexist", "articleCode1": article.code.code},
            )

    def test_store_unknown_prefix_raises(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        with self.assertRaises(UnboundLocalError), self.assertLogs(
            "django.request", level="ERROR"
        ):
            self.client.post(
                "/movement/store/",
                {"storageCode": "xx123", "articleCode1": article.code.code},
            )

    def test_store_into_inactive_space_is_not_validated(self):
        # Characterization: movementStore does not check whether the target
        # space is active; the article is stored anyway.
        inactive = Storage.objects.create(name="Regal B", typ=self.storage_type)
        inactive.space.active = False
        inactive.space.save()
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": inactive.code.code, "articleCode1": article.code.code},
        )
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertEqual(article.stored, inactive.space)

    def test_store_article_into_own_space_is_not_validated(self):
        # Characterization: self-storage is not prevented.
        container = make_article("Box A", self.container_type, space_active=True)
        response = self.client.post(
            "/movement/store/",
            {"storageCode": container.code.code, "articleCode1": container.code.code},
        )
        self.assertEqual(response.status_code, 200)
        container.refresh_from_db()
        self.assertEqual(container.stored, container.space)


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

    def test_remove_only_reads_first_article(self):
        # Characterization: movementRemove only reads `articleCode1`; a second
        # buffered article is ignored.
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
        self.assertEqual(second.stored, self.storage.space)

    def test_remove_unknown_code_raises(self):
        with self.assertRaises(Article.DoesNotExist), self.assertLogs(
            "django.request", level="ERROR"
        ):
            self.client.post("/movement/remove/", {"articleCode1": "a0doesnotexist"})
