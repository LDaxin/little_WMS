from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from organisation.middleware import UserLanguageMiddleware
from organisation.models import Organisation, UserProfile


class UserLanguageTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        self.user = User.objects.create_user("u", password="pw")
        self.profile = UserProfile.objects.create(user=self.user, organisation=self.org)

    def test_default_language_empty(self):
        self.assertEqual(self.profile.language, "")

    def test_middleware_sets_language_code(self):
        self.profile.language = "en"
        self.profile.save()
        request = RequestFactory().get("/")
        SessionMiddleware(lambda r: None).process_request(request)
        request.user = self.user
        UserLanguageMiddleware(lambda r: None)(request)
        self.assertEqual(request.LANGUAGE_CODE, "en")

    def test_middleware_ignores_anonymous(self):
        from django.contrib.auth.models import AnonymousUser

        request = RequestFactory().get("/")
        request.user = AnonymousUser()
        UserLanguageMiddleware(lambda r: None)(request)
        self.assertFalse(hasattr(request, "LANGUAGE_CODE"))


class LanguageApplyTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        self.user = User.objects.create_user("u", password="pw")
        self.client.login(username="u", password="pw")

    def test_language_applied_after_save(self):
        # The user has no profile yet; the view creates one.
        self.client.post("/email-preferences/", {"language": "de"})
        self.assertEqual(UserProfile.objects.get(user=self.user).language, "de")
        response = self.client.get("/")
        self.assertContains(response, "Übersicht")
