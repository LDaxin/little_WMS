from django.contrib.auth.models import User
from django.test import TestCase

from hub.models import Settings
from organisation.models import Invitation, Organisation, OrganisationRequest


class RegistrationTest(TestCase):
    def _set_policy(self, policy):
        settings = Settings.objects.first() or Settings.objects.create()
        settings.registration_policy = policy
        settings.save()

    def test_open_registration(self):
        self._set_policy("open")
        response = self.client.post("/register/", {
            "name": "Pfadfinder", "username": "admin", "email": "a@b.st", "password": "pw",
        })
        self.assertEqual(response.status_code, 302)
        organisation = Organisation.objects.get(name="Pfadfinder")
        self.assertTrue(organisation.roles.filter(name="Admin").exists())
        self.assertTrue(User.objects.filter(username="admin").exists())

    def test_request_registration(self):
        self._set_policy("request")
        self.client.post("/register/", {
            "name": "Pfadfinder", "email": "a@b.st", "reason": "We need it",
        })
        request = OrganisationRequest.objects.get()
        self.assertEqual(request.status, "pending")
        self.assertEqual(request.reason, "We need it")

    def test_invite_only(self):
        self._set_policy("invite")
        self.assertContains(self.client.get("/register/"), "invite-only")

    def test_approve_creates_org(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")
        request = OrganisationRequest.objects.create(name="Pfadfinder", email="a@b.st", reason="x")
        self.client.post("/organisation-requests/%s/review/" % request.pk, {"action": "approve"})
        request.refresh_from_db()
        self.assertEqual(request.status, "approved")
        self.assertTrue(Organisation.objects.filter(name="Pfadfinder").exists())
        self.assertTrue(Invitation.objects.filter(email="a@b.st").exists())

    def test_reject_does_not_create_org(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")
        request = OrganisationRequest.objects.create(name="Pfadfinder", email="a@b.st", reason="x")
        self.client.post("/organisation-requests/%s/review/" % request.pk, {"action": "reject"})
        request.refresh_from_db()
        self.assertEqual(request.status, "rejected")
        self.assertFalse(Organisation.objects.filter(name="Pfadfinder").exists())

    def test_review_requires_superuser(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/organisation-requests/").status_code, 403)
