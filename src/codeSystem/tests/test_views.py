from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datastructures import MultiValueDictKeyError

from article.models import Article, ArticleBase, ArticleType
from codeSystem.models import UuidCode
from location.models import Location
from storage.models import Storage, StorageType


class CodeSystemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_pages_return_200(self):
        urls = [
            "/code/",
            "/code/search?search=",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_add_modal_url_is_shadowed(self):
        # Characterization: `^code/add` is registered before `^code/add/modal`,
        # so GET /code/add/modal is routed to addCode and raises
        # MultiValueDictKeyError (HTTP 500). The addModal view is unreachable.
        with self.assertRaises(MultiValueDictKeyError), self.assertLogs(
            "django.request", level="ERROR"
        ):
            self.client.get("/code/add/modal")

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/code/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_add_codes(self):
        response = self.client.post("/code/add", {"types": "1", "number": "3"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UuidCode.objects.filter(prefix="a0", used=False).count(), 3)

    def test_export_codes(self):
        code = UuidCode.objects.create(prefix="a0", used=False)
        response = self.client.post("/code/export", {f"_{code.pk}": str(code.pk)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv; charset=iso-8859-1")


class CanonicalLinkTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)
        cls.location = Location.objects.create(
            traditionalLand="Deutschland",
            traditionalCountry="DE",
            traditionalCity="Berlin",
            traditionalZipcode="10115",
            traditionalStreet="Invalidenstr.",
            traditionalStreetNumber="1",
        )

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_article_code_redirects(self):
        response = self.client.get("/a/%s" % self.article.code.code)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/article/werkzeug/%s" % self.article.pk)

    def test_storage_code_redirects(self):
        response = self.client.get("/s/%s" % self.storage.code.code)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/storage/regal/%s" % self.storage.pk)

    def test_location_code_redirects(self):
        response = self.client.get("/l/%s" % self.location.code.code)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/location/%s" % self.location.pk)

    def test_unknown_code_returns_404(self):
        with self.assertLogs("django.request", level="WARNING"):
            response = self.client.get("/a/a0doesnotexist")
        self.assertEqual(response.status_code, 404)
