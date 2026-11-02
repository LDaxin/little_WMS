from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from hub.toasts import toast


class ToastTest(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.request.user = AnonymousUser()

    def test_error_toast(self):
        content = toast(self.request, "Error", "boom", "alert").content.decode()
        self.assertIn("boom", content)
        self.assertIn("errorToast", content)

    def test_success_toast(self):
        content = toast(self.request, "Success", "done", "status").content.decode()
        self.assertIn("done", content)
        self.assertIn("successToast", content)
