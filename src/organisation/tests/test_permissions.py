from django.contrib.auth.models import User
from django.test import TestCase

from organisation.models import Organisation, Role, UserProfile
from organisation.permissions import (
    PERMISSIONS,
    ROLE_TEMPLATES,
    all_permissions,
    ensure_role_templates,
    has_perm,
)


class PermissionCatalogTest(TestCase):
    def test_all_permissions_format(self):
        perms = all_permissions()
        self.assertIn("article.view_all", perms)
        self.assertIn("article.move_assigned", perms)
        self.assertIn("export.qr_sheet_all", perms)
        self.assertEqual(len(perms), len(set(perms)))

    def test_every_object_covered(self):
        for obj in PERMISSIONS:
            self.assertTrue(any(p.startswith(obj + ".") for p in all_permissions()))


class HasPermTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.get(pk=1)
        self.role = Role.objects.create(
            organisation=self.org, name="Tester", permissions={"article": ["view_all"]}
        )
        self.user = User.objects.create_user("tester", password="pw")
        UserProfile.objects.create(user=self.user, role=self.role, organisation=self.org)

    def test_superuser_has_everything(self):
        admin = User.objects.create_superuser("admin", "a@b.c", "pw")
        self.assertTrue(has_perm(admin, "article.delete_all"))

    def test_role_permission_granted(self):
        self.assertTrue(has_perm(self.user, "article.view_all"))

    def test_role_permission_denied(self):
        self.assertFalse(has_perm(self.user, "article.delete_all"))

    def test_no_profile_denied(self):
        other = User.objects.create_user("other", password="pw")
        self.assertFalse(has_perm(other, "article.view_all"))

    def test_anonymous_denied(self):
        from django.contrib.auth.models import AnonymousUser

        self.assertFalse(has_perm(AnonymousUser(), "article.view_all"))


class RoleTemplateTest(TestCase):
    def test_templates_seeded_for_default_org(self):
        templates = Role.objects.filter(organisation_id=1, is_template=True)
        self.assertEqual(templates.count(), len(ROLE_TEMPLATES))
        self.assertTrue(templates.filter(name="Full Access").exists())

    def test_full_access_has_all_permissions(self):
        role = Role.objects.get(organisation_id=1, name="Full Access")
        self.assertIn("delete_all", role.permissions["article"])
        self.assertIn("move_assigned", role.permissions["article"])

    def test_ensure_role_templates_idempotent(self):
        org = Organisation.objects.create(name="Neu", slug="neu")
        ensure_role_templates(org)
        ensure_role_templates(org)
        self.assertEqual(org.roles.filter(is_template=True).count(), len(ROLE_TEMPLATES))
