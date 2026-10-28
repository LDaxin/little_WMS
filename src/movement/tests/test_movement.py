from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from audit.models import AuditLog
from movement.models import MovementSession
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


class WhereTest(MovementTestBase):
    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/where/").status_code, 200)

    def test_by_code(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=self.storage.space, menge=1)
        response = self.client.get("/where/", {"q": article.code.code})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hammer")
        self.assertContains(response, "Regal A")

    def test_by_name(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.get("/where/", {"q": "Hammer"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.code.code)

    def test_unknown(self):
        response = self.client.get("/where/", {"q": "nope"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No article found")

    def test_search_suggestions(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        response = self.client.get("/where/search", {"q": "Hammer"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.code.code)


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
        self.assertTrue(article.stocks.filter(stored=self.storage.space).exists())
        self.assertEqual(self.state()["buffer"], [])

    def test_store_without_target(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.scan(article.code.code)
        response = self.client.post("/movement/store/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unknown code")
        self.assertFalse(article.stocks.filter(stored=self.storage.space).exists())

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
        self.assertFalse(article.stocks.filter(stored=inactive.space).exists())


class MovementRemoveTest(MovementTestBase):
    def test_remove_buffered_articles(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=self.storage.space, menge=1)
        self.scan(article.code.code)
        response = self.client.post("/movement/remove/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(article.stocks.filter(stored=self.storage.space).exists())
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


class MovementSessionUndoTest(MovementTestBase):
    def store(self, article):
        self.scan(self.storage.code.code)
        self.scan(article.code.code)
        return self.client.post("/movement/store/")

    def test_store_creates_session_and_links_entry(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.store(article)
        session = MovementSession.objects.get(user=self.user, ended_at=None)
        entry = AuditLog.objects.get(action="moved")
        self.assertEqual(entry.session, session)

    def test_undo_moved_returns_article(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.store(article)
        self.assertTrue(article.stocks.filter(stored=self.storage.space).exists())
        response = self.client.post("/movement/undo/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(article.stocks.filter(stored=self.storage.space).exists())
        self.assertTrue(article.stocks.filter(stored=None).exists())
        self.assertTrue(AuditLog.objects.get(action="moved").undone)

    def test_undo_removed_stores_article_back(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        Stock.objects.create(article=article, stored=self.storage.space, menge=1)
        self.scan(article.code.code)
        self.client.post("/movement/remove/")
        self.assertFalse(article.stocks.filter(stored=self.storage.space).exists())
        self.client.post("/movement/undo/")
        self.assertTrue(article.stocks.filter(stored=self.storage.space).exists())

    def test_undo_entry_by_id(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.store(article)
        entry = AuditLog.objects.get(action="moved")
        self.client.post("/movement/undo/entry/", {"entry": entry.pk})
        self.assertFalse(article.stocks.filter(stored=self.storage.space).exists())

    def test_undo_without_session_shows_error(self):
        response = self.client.post("/movement/undo/")
        self.assertContains(response, "Nothing to undo")

    def test_session_list_rendered(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.store(article)
        response = self.client.get("/movement/")
        self.assertContains(response, "Session")
        self.assertContains(response, "Undo last action")

    def test_clear_ends_session(self):
        article = make_article("Hammer", self.article_type, space_active=False)
        self.store(article)
        self.client.post("/movement/clear/")
        self.assertFalse(MovementSession.objects.filter(user=self.user, ended_at=None).exists())
