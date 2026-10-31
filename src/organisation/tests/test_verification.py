from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings

from hub.models import Settings
from organisation.models import EmailVerification, Invitation
from organisation.verification import is_verified, request_verification, verify


class VerificationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", "u@example.com", "pw")

    @override_settings(EMAIL_CONFIGURED=True)
    def test_request_creates_record_and_sends(self):
        record = request_verification(self.user)
        self.assertFalse(record.verified)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/verify-email/", mail.outbox[0].body)

    def test_request_without_email(self):
        user = User.objects.create_user("noemail", "", "pw")
        self.assertIsNone(request_verification(user))
        self.assertFalse(EmailVerification.objects.filter(user=user).exists())

    def test_verify_marks_verified(self):
        record = request_verification(self.user)
        self.assertTrue(verify(record.token).verified)
        self.assertTrue(is_verified("u@example.com"))

    def test_verify_unknown_token(self):
        self.assertIsNone(verify("nope"))
        self.assertFalse(is_verified("u@example.com"))

    def test_resend_issues_new_token(self):
        first = request_verification(self.user)
        second = request_verification(self.user)
        self.assertNotEqual(first.token, second.token)
        self.assertFalse(second.verified)


class VerificationFlowTest(TestCase):
    @override_settings(EMAIL_CONFIGURED=True)
    def test_register_sends_verification(self):
        Settings.objects.create(registration_policy="open")
        self.client.post("/register/", {
            "name": "Org", "username": "new", "email": "new@example.com", "password": "pw",
        })
        user = User.objects.get(username="new")
        self.assertTrue(EmailVerification.objects.filter(user=user).exists())
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_CONFIGURED=True)
    def test_invite_accept_sends_verification(self):
        invitation = Invitation.objects.create(organisation_id=1)
        self.client.post(f"/invite/{invitation.token}/", {
            "username": "newbie", "email": "new@example.com", "password": "pw", "password2": "pw",
        })
        user = User.objects.get(username="newbie")
        self.assertTrue(EmailVerification.objects.filter(user=user).exists())

    def test_verify_link(self):
        user = User.objects.create_user("u", "u@example.com", "pw")
        record = request_verification(user)
        response = self.client.get(f"/verify-email/{record.token}/")
        self.assertContains(response, "confirmed")
        record.refresh_from_db()
        self.assertTrue(record.verified)

    def test_verify_link_invalid(self):
        response = self.client.get("/verify-email/nope/")
        self.assertContains(response, "invalid")
