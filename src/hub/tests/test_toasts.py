from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from hub.toasts import error_toast, success_toast, toast


class ToastTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.user = AnonymousUser()

    def test_error_toast(self):
        content = toast(self.request, "Error", "boom", "alert").content.decode()
        self.assertIn("boom", content)
        self.assertIn("errorToast", content)

    def test_success_toast(self):
        content = success_toast(self.request, "done").content.decode()
        self.assertIn("done", content)
        self.assertIn("successToast", content)

    def test_error_shortcut(self):
        self.assertIn("errorToast", error_toast(self.request, "nope").content.decode())
