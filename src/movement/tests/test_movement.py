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


class MovementTestBase(TestCase):
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

    def scan(self, code):
        return self.client.post("/movement/scan/", {"code": code})

    def state(self):
        return self.client.session.get("movement")


class MovementViewTest(MovementTestBase):
    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/movement/").status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/movement/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_search(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.get("/movement/search/", {"search": "Hammer"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.code.code)

    def test_search_missing_param(self):
        self.assertEqual(self.client.get("/movement/search/").status_code, 200)


class MovementScanTest(MovementTestBase):
    def test_scan_storage_sets_target(self):
        self.scan(self.storage.code.code)
        self.assertEqual(self.state()["target"], self.storage.code.code)
        self.assertFalse(self.state()["target_smart"])

    def test_scan_article_buffers(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(article.code.code)
        self.assertIn(article.code.code, self.state()["buffer"])

    def test_scan_container_smart_default(self):
        container = make_article("Box A", self.container_type, space_active=True)
        self.scan(container.code.code)
        self.assertEqual(self.state()["target"], container.code.code)
        self.assertTrue(self.state()["target_smart"])

    def test_scan_container_with_target_buffers(self):
        container = make_article("Box A", self.container_type, space_active=True)
        self.scan(self.storage.code.code)
        self.scan(container.code.code)
        self.assertIn(container.code.code, self.state()["buffer"])

    def test_scan_unknown_prefix(self):
        response = self.scan("xx123")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown code")

    def test_scan_unknown_article(self):
        response = self.scan("a0doesnotexist")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No object with code")


class MovementStoreTest(MovementTestBase):
    def test_store_buffered_articles(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(self.storage.code.code)
        self.scan(article.code.code)
        response = self.client.post("/movement/store/")
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertEqual(article.stored, self.storage.space)
        self.assertEqual(self.state()["buffer"], [])

    def test_store_without_target(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(article.code.code)
        response = self.client.post("/movement/store/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown code")
        article.refresh_from_db()
        self.assertIsNone(article.stored)

    def test_store_into_inactive_space(self):
        inactive = Storage.objects.create(name="Regal B", typ=self.storage_type)
        inactive.space.active = False
        inactive.space.save()
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(inactive.code.code)
        self.scan(article.code.code)
        response = self.client.post("/movement/store/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "not active")
        article.refresh_from_db()
        self.assertIsNone(article.stored)


class MovementRemoveTest(MovementTestBase):
    def test_remove_buffered_articles(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        article.stored = self.storage.space
        article.save()
        self.scan(article.code.code)
        response = self.client.post("/movement/remove/")
        self.assertEqual(response.status_code, 200)
        article.refresh_from_db()
        self.assertIsNone(article.stored)
        self.assertEqual(self.state()["buffer"], [])


class MovementBufferActionsTest(MovementTestBase):
    def test_mode_change_clears_buffer(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(article.code.code)
        self.client.post("/movement/mode/", {"mode": "remove"})
        self.assertEqual(self.state()["mode"], "remove")
        self.assertEqual(self.state()["buffer"], [])

    def test_clear(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(article.code.code)
        self.client.post("/movement/clear/")
        self.assertEqual(self.state()["buffer"], [])

    def test_buffer_remove(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(article.code.code)
        self.client.post("/movement/buffer/remove/", {"code": article.code.code})
        self.assertEqual(self.state()["buffer"], [])

    def test_treat_as_article(self):
        container = make_article("Box A", self.container_type, space_active=True)
        self.scan(container.code.code)
        self.client.post("/movement/treat-as-article/")
        self.assertIsNone(self.state()["target"])
        self.assertIn(container.code.code, self.state()["buffer"])

    def test_set_target(self):
        container = make_article("Box A", self.container_type, space_active=True)
        self.scan(self.storage.code.code)
        self.scan(container.code.code)
        self.client.post("/movement/set-target/", {"code": container.code.code})
        self.assertEqual(self.state()["target"], container.code.code)
        self.assertNotIn(container.code.code, self.state()["buffer"])
