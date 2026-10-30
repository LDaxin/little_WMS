from datetime import timedelta

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.utils import timezone

from organisation.models import Invitation, Organisation, Role, UserProfile


def manager(username):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Manager " + username)
    role.permissions.set(
        Permission.objects.filter(codename__in=["user_view_all", "user_invite_all"])
    )
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class InvitationModelTest(TestCase):
    def test_token_and_default_expiry(self):
        invitation = Invitation.objects.create(organisation_id=1)
        self.assertTrue(invitation.token)
        self.assertAlmostEqual(
            (invitation.expires_at - timezone.now()).total_seconds(), 7 * 86400, delta=60
        )
        self.assertTrue(invitation.is_valid())

    def test_expired_is_invalid(self):
        invitation = Invitation.objects.create(
            organisation_id=1, expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertFalse(invitation.is_valid())

    def test_accepted_is_invalid(self):
        invitation = Invitation.objects.create(organisation_id=1, status="accepted")
        self.assertFalse(invitation.is_valid())


class InviteCreateTest(TestCase):
    def setUp(self):
        self.user = manager("boss")
        self.client.login(username="boss", password="pw")

    def test_create_invitation(self):
        self.client.post("/invitations/create/", {"days": "3"})
        invitation = Invitation.objects.get()
        self.assertEqual(invitation.organisation_id, 1)
        self.assertEqual(invitation.invited_by, self.user)

    def test_requires_permission(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.post("/invitations/create/", {}).status_code, 403)

    def test_revoke(self):
        invitation = Invitation.objects.create(organisation_id=1)
        self.client.post(f"/invitations/{invitation.pk}/revoke/")
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, "revoked")


class InviteAcceptTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(organisation_id=1, name="Helper")
        self.invitation = Invitation.objects.create(organisation_id=1, role=self.role)

    def test_accept_as_new_user(self):
        response = self.client.post(
            f"/invite/{self.invitation.token}/",
            {"username": "newbie", "password": "pw"},
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="newbie")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.organisation_id, 1)
        self.assertEqual(profile.role, self.role)
        self.invitation.refresh_from_db()
        self.assertEqual(self.invitation.status, "accepted")

    def test_accept_as_existing_user(self):
        user = User.objects.create_user("existing", password="pw")
        self.client.login(username="existing", password="pw")
        response = self.client.get(f"/invite/{self.invitation.token}/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserProfile.objects.filter(user=user, organisation_id=1).exists())

    def test_accept_when_already_member(self):
        user = User.objects.create_user("member", password="pw")
        UserProfile.objects.create(user=user, organisation_id=1)
        self.client.login(username="member", password="pw")
        self.client.get(f"/invite/{self.invitation.token}/")
        self.assertEqual(UserProfile.objects.filter(user=user, organisation_id=1).count(), 1)

    def test_reject_expired(self):
        self.invitation.expires_at = timezone.now() - timedelta(days=1)
        self.invitation.save()
        response = self.client.get(f"/invite/{self.invitation.token}/")
        self.assertContains(response, "no longer valid")

    def test_reject_revoked(self):
        self.invitation.status = "revoked"
        self.invitation.save()
        response = self.client.get(f"/invite/{self.invitation.token}/")
        self.assertContains(response, "no longer valid")
