from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from occasion.models import OccasionType
from organisation.models import Role, UserProfile


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class TrashTest(TestCase):
    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")
        self.ct_id = ContentType.objects.get_for_model(OccasionType).pk

    def test_list_restore_delete(self):
        occ_type = OccasionType.objects.create(name="Camp")
        occ_type.delete()

        self.assertContains(self.client.get("/trash/"), "Camp")

        self.client.post("/trash/%s/%s/restore/" % (self.ct_id, occ_type.pk))
        occ_type.refresh_from_db()
        self.assertIsNone(occ_type.deleted_at)

        occ_type.delete()
        self.client.post("/trash/%s/%s/delete/" % (self.ct_id, occ_type.pk))
        self.assertFalse(
            OccasionType.objects.all_with_deleted().filter(pk=occ_type.pk).exists()
        )

    def test_view_permission(self):
        user_with("nobody", "article_view_all")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/trash/").status_code, 403)

    def test_restore_permission(self):
        occ_type = OccasionType.objects.create(name="Camp")
        occ_type.delete()
        user_with("viewer", "trash_view_all")
        self.client.login(username="viewer", password="pw")
        response = self.client.post("/trash/%s/%s/restore/" % (self.ct_id, occ_type.pk))
        self.assertEqual(response.status_code, 403)

    def test_delete_forever_permission(self):
        occ_type = OccasionType.objects.create(name="Camp")
        occ_type.delete()
        user_with("viewer", "trash_view_all", "trash_restore_all")
        self.client.login(username="viewer", password="pw")
        response = self.client.post("/trash/%s/%s/delete/" % (self.ct_id, occ_type.pk))
        self.assertEqual(response.status_code, 403)
