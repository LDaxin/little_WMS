from django.contrib.auth.models import Permission, User
from django.core import mail
from django.test import TestCase, override_settings

from organisation.models import Role, UserProfile


def manager(username):
    """A user with the permissions to view users and manage roles (§3)."""
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Manager " + username)
    role.permissions.set(
        Permission.objects.filter(codename__in=["user_view_all", "user_edit_role_all"])
    )
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class RolesViewTest(TestCase):
    def setUp(self):
        self.user = manager("tester")
        self.client.login(username="tester", password="pw")

    def test_roles_page_returns_200(self):
        self.assertEqual(self.client.get("/roles/").status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        self.assertEqual(self.client.get("/roles/").status_code, 302)

    def test_requires_permission(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/roles/").status_code, 403)
        self.assertEqual(self.client.post("/roles/create/", {"template": "Read Only"}).status_code, 403)

    def test_create_from_template(self):
        self.client.post("/roles/create/", {"template": "Read Only", "name": "Praktikant"})
        role = Role.objects.get(name="Praktikant")
        self.assertFalse(role.is_template)
        self.assertTrue(role.permissions.filter(codename="article_view_all").exists())

    def test_create_from_template_with_default_name(self):
        # KI-020: the default name equals the template name and used to collide
        response = self.client.post("/roles/create/", {"template": "Read Only", "name": "Read Only"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Role.objects.filter(name="Read Only", is_template=False).exists())

    def test_create_duplicate_role_shows_error(self):
        Role.objects.create(organisation_id=1, name="Praktikant")
        response = self.client.post("/roles/create/", {"template": "Read Only", "name": "Praktikant"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")
        self.assertEqual(Role.objects.filter(name="Praktikant", is_template=False).count(), 1)

    def test_role_detail_shows_matrix(self):
        role = Role.objects.create(organisation_id=1, name="Tester")
        response = self.client.get(f"/roles/{role.pk}/")
        self.assertContains(response, "article")
        self.assertContains(response, "view_all")

    def test_role_save_updates_permissions(self):
        role = Role.objects.create(organisation_id=1, name="Tester")
        self.client.post(
            f"/roles/{role.pk}/save/",
            {"perm": ["article_view_all", "storage_view_all"]},
        )
        codenames = set(role.permissions.values_list("codename", flat=True))
        self.assertEqual(codenames, {"article_view_all", "storage_view_all"})

    def test_role_delete(self):
        role = Role.objects.create(organisation_id=1, name="Tester")
        self.client.post(f"/roles/{role.pk}/delete/")
        self.assertFalse(Role.objects.filter(pk=role.pk).exists())

    def test_template_cannot_be_deleted(self):
        template = Role.objects.get(organisation_id=1, name="Read Only")
        response = self.client.post(f"/roles/{template.pk}/delete/")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Role.objects.filter(pk=template.pk).exists())


class UserRoleViewTest(TestCase):
    def setUp(self):
        self.user = manager("tester")
        self.client.login(username="tester", password="pw")
        self.role = Role.objects.create(organisation_id=1, name="Tester")

    def test_users_page_returns_200(self):
        self.assertEqual(self.client.get("/users/").status_code, 200)

    def test_requires_permission(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/users/").status_code, 403)

    def test_assign_role(self):
        self.client.post(f"/users/{self.user.pk}/role/", {"role": self.role.pk})
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.role, self.role)

    def test_clear_role(self):
        self.client.post(f"/users/{self.user.pk}/role/", {"role": ""})
        self.assertIsNone(UserProfile.objects.get(user=self.user).role)


class ServerSettingsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("root", "root@example.com", "pw")
        self.client.login(username="root", password="pw")

    @override_settings(EMAIL_CONFIGURED=False)
    def test_page_shows_status(self):
        response = self.client.get("/server-settings/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "not configured")

    @override_settings(EMAIL_CONFIGURED=True)
    def test_send_test_email(self):
        response = self.client.post("/server-settings/", {"action": "test_email"})
        self.assertContains(response, "Test email sent")
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_CONFIGURED=False)
    def test_test_email_not_configured(self):
        response = self.client.post("/server-settings/", {"action": "test_email"})
        self.assertContains(response, "not configured")
        self.assertEqual(len(mail.outbox), 0)
