from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.datastructures import MultiValueDictKeyError

from codeSystem.models import UuidCode


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
