from django.contrib.auth.models import Permission, User
from django.contrib.sessions.backends.db import SessionStore
from django.db import IntegrityError
from django.test import RequestFactory, TestCase

from organisation.models import Organisation, Role, UserProfile
from organisation.permissions import has_perm
from organisation.services import active_organisation, set_active_organisation


class MembershipModelTest(TestCase):
    def test_user_can_belong_to_multiple_orgs(self):
        user = User.objects.create_user("tester", password="pw")
        org_a = Organisation.objects.create(name="A", slug="a")
        org_b = Organisation.objects.create(name="B", slug="b")
        UserProfile.objects.create(user=user, organisation=org_a)
        UserProfile.objects.create(user=user, organisation=org_b)
        self.assertEqual(user.profiles.count(), 2)

    def test_unique_user_org(self):
        user = User.objects.create_user("tester", password="pw")
        UserProfile.objects.create(user=user, organisation_id=1)
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(user=user, organisation_id=1)


class ActiveOrganisationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user("tester", password="pw")
        self.org_a = Organisation.objects.create(name="A", slug="a")
        self.org_b = Organisation.objects.create(name="B", slug="b")

    def request(self):
        request = self.factory.get("/")
        request.user = self.user
        request.session = SessionStore()
        return request

    def test_falls_back_to_first_membership(self):
        UserProfile.objects.create(user=self.user, organisation=self.org_a)
        self.assertEqual(active_organisation(self.request()), self.org_a)

    def test_session_wins(self):
        UserProfile.objects.create(user=self.user, organisation=self.org_a)
        request = self.request()
        set_active_organisation(request, self.org_b)
        self.assertEqual(active_organisation(request), self.org_b)

    def test_default_when_no_membership(self):
        self.assertEqual(active_organisation(self.request()).pk, 1)


class SelectOrganisationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.client.login(username="tester", password="pw")
        self.org_a = Organisation.objects.create(name="A", slug="a")
        self.org_b = Organisation.objects.create(name="B", slug="b")

    def test_single_org_redirects_to_hub(self):
        UserProfile.objects.create(user=self.user, organisation=self.org_a)
        self.assertRedirects(self.client.get("/select-organisation/"), "/")

    def test_multiple_orgs_shows_chooser(self):
        UserProfile.objects.create(user=self.user, organisation=self.org_a)
        UserProfile.objects.create(user=self.user, organisation=self.org_b)
        response = self.client.get("/select-organisation/")
        self.assertContains(response, "A")
        self.assertContains(response, "B")

    def test_no_org_creates_default(self):
        self.assertRedirects(self.client.get("/select-organisation/"), "/")
        self.assertTrue(UserProfile.objects.filter(user=self.user, organisation_id=1).exists())

    def test_switch_sets_session(self):
        UserProfile.objects.create(user=self.user, organisation=self.org_a)
        response = self.client.post("/switch-organisation/", {"organisation": self.org_a.pk})
        self.assertRedirects(response, "/")
        self.assertEqual(self.client.session["active_organisation_id"], self.org_a.pk)

    def test_switch_rejects_foreign_org(self):
        response = self.client.post("/switch-organisation/", {"organisation": self.org_b.pk})
        self.assertEqual(response.status_code, 404)


class HasPermPerOrgTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.org_a = Organisation.objects.create(name="A", slug="a")
        self.org_b = Organisation.objects.create(name="B", slug="b")
        role_a = Role.objects.create(organisation=self.org_a, name="Admin")
        role_a.permissions.set(Permission.objects.filter(codename="article_view_all"))
        role_b = Role.objects.create(organisation=self.org_b, name="Helper")
        UserProfile.objects.create(user=self.user, organisation=self.org_a, role=role_a)
        UserProfile.objects.create(user=self.user, organisation=self.org_b, role=role_b)

    def test_role_per_org(self):
        self.assertTrue(has_perm(self.user, "article.view_all", self.org_a))
        self.assertFalse(has_perm(self.user, "article.view_all", self.org_b))
