from django.contrib.auth.models import User
from django.test import TestCase

from organisation.models import Role, UserProfile


class RolesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_roles_page_returns_200(self):
        self.assertEqual(self.client.get("/roles/").status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get("/roles/").status_code, 302)

    def test_create_from_template(self):
        self.client.post("/roles/create/", {"template": "Read Only", "name": "Praktikant"})
        role = Role.objects.get(name="Praktikant")
        self.assertFalse(role.is_template)
        self.assertIn("view_all", role.permissions["article"])

    def test_role_detail_shows_matrix(self):
        role = Role.objects.create(organisation_id=1, name="Tester", permissions={})
        response = self.client.get(f"/roles/{role.pk}/")
        self.assertContains(response, "article")
        self.assertContains(response, "view_all")

    def test_role_save_updates_permissions(self):
        role = Role.objects.create(organisation_id=1, name="Tester", permissions={})
        self.client.post(f"/roles/{role.pk}/save/", {"perm": ["article.view_all", "storage.view_all"]})
        role.refresh_from_db()
        self.assertEqual(role.permissions["article"], ["view_all"])
        self.assertEqual(role.permissions["storage"], ["view_all"])

    def test_role_delete(self):
        role = Role.objects.create(organisation_id=1, name="Tester", permissions={})
        self.client.post(f"/roles/{role.pk}/delete/")
        self.assertFalse(Role.objects.filter(pk=role.pk).exists())

    def test_template_cannot_be_deleted(self):
        template = Role.objects.get(organisation_id=1, name="Read Only")
        response = self.client.post(f"/roles/{template.pk}/delete/")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Role.objects.filter(pk=template.pk).exists())


class UserRoleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw")
        self.client.login(username="tester", password="pw")
        self.role = Role.objects.create(organisation_id=1, name="Tester", permissions={})

    def test_users_page_returns_200(self):
        self.assertEqual(self.client.get("/users/").status_code, 200)

    def test_assign_role(self):
        self.client.post(f"/users/{self.user.pk}/role/", {"role": self.role.pk})
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.role, self.role)

    def test_clear_role(self):
        UserProfile.objects.create(user=self.user, role=self.role, organisation_id=1)
        self.client.post(f"/users/{self.user.pk}/role/", {"role": ""})
        self.assertIsNone(UserProfile.objects.get(user=self.user).role)
