from django.contrib.auth.models import Permission, User
from django.test import TestCase

import json

from article.models import Article, ArticleBase, ArticleType
from location.models import Location
from organisation.models import Organisation, Role, UserProfile
from storage.models import StorageType
from tag.models import Tag


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


class ApiWriteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")

    def test_create_location(self):
        user_with(self.org, "u", "location_create_all")
        self.client.login(username="u", password="pw")
        response = self.client.post(
            "/api/v1/locations/", {"line1": "Musterstrasse 1", "city": "Musterstadt"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Location.objects.filter(line1="Musterstrasse 1").exists())

    def test_update_tag(self):
        user_with(self.org, "u", "tag_edit_all")
        self.client.login(username="u", password="pw")
        tag = Tag.objects.create(name="Sommer", organisation=self.org)
        response = self.client.patch(
            "/api/v1/tags/%s/" % tag.pk,
            json.dumps({"name": "Winter"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        tag.refresh_from_db()
        self.assertEqual(tag.name, "Winter")

    def test_delete_storage_type_soft_deletes(self):
        user_with(self.org, "u", "storage_delete_all")
        self.client.login(username="u", password="pw")
        storage_type = StorageType.objects.create(name="Regal", symbol="RE", organisation=self.org)
        response = self.client.delete("/api/v1/storage-types/%s/" % storage_type.pk)
        self.assertEqual(response.status_code, 204)
        storage_type.refresh_from_db()
        self.assertIsNotNone(storage_type.deleted_at)

    def test_write_permission(self):
        user_with(self.org, "u", "location_view_all")
        self.client.login(username="u", password="pw")
        response = self.client.post("/api/v1/locations/", {"line1": "X"})
        self.assertEqual(response.status_code, 403)
