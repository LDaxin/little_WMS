from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from organisation.models import Organisation, Role, UserProfile


def user_with(organisation, username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation=organisation, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, organisation=organisation, role=role)
    return user


class ApiTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type, organisation=cls.org)
        cls.article = Article.objects.create(base=cls.base, organisation=cls.org)

    def test_requires_auth(self):
        response = self.client.get("/api/v1/articles/")
        self.assertIn(response.status_code, (401, 403))

    def test_list_articles(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        response = self.client.get("/api/v1/articles/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_article(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        response = self.client.get("/api/v1/articles/%s/" % self.article.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.article.pk)

    def test_missing_permission(self):
        user_with(self.org, "u", "storage_view_all")
        self.client.login(username="u", password="pw")
        self.assertEqual(self.client.get("/api/v1/articles/").status_code, 403)
