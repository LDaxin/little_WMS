from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.utils import timezone

from article.models import Article, ArticleBase, ArticleType
from organisation.models import Organisation, Role, UserProfile
from savedviews.models import SavedView, ShareLink


def user_with(organisation, username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation=organisation, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, organisation=organisation, role=role)
    return user


class SavedViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")

    def setUp(self):
        self.user = user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")

    def test_save_view(self):
        self.client.post("/views/save/", {
            "name": "My view", "query": '{"type": "AND", "conditions": []}', "typ": "tent",
        })
        view = SavedView.objects.get()
        self.assertEqual(view.name, "My view")
        self.assertEqual(view.owner, self.user)
        self.assertEqual(view.typ, "tent")

    def test_list_own_and_shared(self):
        SavedView.objects.create(owner=self.user, name="Mine", typ="tent", organisation=self.org)
        other = User.objects.create_user("other", password="pw")
        SavedView.objects.create(owner=other, name="Shared", typ="tent", is_shared=True, organisation=self.org)
        SavedView.objects.create(owner=other, name="Private", typ="tent", is_shared=False, organisation=self.org)
        response = self.client.get("/views/")
        self.assertContains(response, "Mine")
        self.assertContains(response, "Shared")
        self.assertNotContains(response, "Private")

    def test_delete(self):
        view = SavedView.objects.create(owner=self.user, name="Mine", typ="tent", organisation=self.org)
        self.client.post("/views/%s/delete/" % view.pk)
        view.refresh_from_db()
        self.assertIsNotNone(view.deleted_at)


class ShareLinkTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        article_type = ArticleType.objects.create(name="tent", symbol="TZ", organisation=cls.org)
        base = ArticleBase.objects.create(name="Jurte", pType=article_type, organisation=cls.org)
        Article.objects.create(base=base, organisation=cls.org)

    def setUp(self):
        self.user = user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        self.view = SavedView.objects.create(
            owner=self.user, name="Mine", typ="tent", organisation=self.org,
            query={"type": "AND", "conditions": []},
        )

    def test_create_link(self):
        self.client.post("/views/%s/share/" % self.view.pk, {"access_mode": "public"})
        link = ShareLink.objects.get()
        self.assertTrue(link.token)
        self.assertTrue(link.is_active)

    def test_open_valid_link(self):
        link = ShareLink.objects.create(saved_view=self.view)
        response = self.client.get("/s/%s/" % link.token)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jurte")

    def test_expired_link(self):
        link = ShareLink.objects.create(saved_view=self.view, expires_at=timezone.now() - timedelta(days=1))
        self.assertContains(self.client.get("/s/%s/" % link.token), "unavailable")

    def test_revoked_link(self):
        link = ShareLink.objects.create(saved_view=self.view, is_active=False)
        self.assertContains(self.client.get("/s/%s/" % link.token), "unavailable")

    def test_single_use(self):
        link = ShareLink.objects.create(saved_view=self.view, single_use=True)
        self.client.get("/s/%s/" % link.token)
        link.refresh_from_db()
        self.assertEqual(link.used_count, 1)
        self.assertContains(self.client.get("/s/%s/" % link.token), "unavailable")

    def test_password(self):
        link = ShareLink.objects.create(saved_view=self.view, password_hash=make_password("secret"))
        self.assertContains(self.client.get("/s/%s/" % link.token), "Password")
        response = self.client.post("/s/%s/" % link.token, {"password": "secret"})
        self.assertEqual(response.status_code, 302)

    def test_revoke(self):
        link = ShareLink.objects.create(saved_view=self.view)
        self.client.post("/share-links/%s/revoke/" % link.pk)
        link.refresh_from_db()
        self.assertFalse(link.is_active)

    def test_borrow_via_link(self):
        from loans.models import Loan

        link = ShareLink.objects.create(
            saved_view=self.view, permissions=["view", "borrow"], requires_confirmation=False
        )
        article = Article.objects.first()
        self.client.post("/s/%s/" % link.token, {"article_%s" % article.pk: "on"})
        self.assertEqual(Loan.objects.get().status, "active")

    def test_borrow_pending(self):
        from loans.models import Loan

        link = ShareLink.objects.create(
            saved_view=self.view, permissions=["view", "borrow"], requires_confirmation=True
        )
        article = Article.objects.first()
        self.client.post("/s/%s/" % link.token, {"article_%s" % article.pk: "on"})
        self.assertEqual(Loan.objects.get().status, "pending")

    def test_no_borrow_without_permission(self):
        from loans.models import Loan

        link = ShareLink.objects.create(saved_view=self.view, permissions=["view"])
        article = Article.objects.first()
        self.client.post("/s/%s/" % link.token, {"article_%s" % article.pk: "on"})
        self.assertFalse(Loan.objects.exists())
