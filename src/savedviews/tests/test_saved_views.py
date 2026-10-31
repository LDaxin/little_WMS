from django.contrib.auth.models import Permission, User
from django.test import TestCase

from organisation.models import Organisation, Role, UserProfile
from savedviews.models import SavedView


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
