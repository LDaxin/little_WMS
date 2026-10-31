from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings

from hub.mail import send
from organisation.models import EmailVerification


class MailServiceTest(TestCase):
    @override_settings(EMAIL_CONFIGURED=False)
    def test_skips_when_not_configured(self):
        with self.assertLogs("hub.mail", level="WARNING"):
            self.assertFalse(send("a@example.com", "Hi", "Body", require_verified=False))
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_CONFIGURED=True)
    def test_sends_when_configured(self):
        self.assertTrue(send("a@example.com", "Hi", "Body", require_verified=False))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["a@example.com"])

    @override_settings(EMAIL_CONFIGURED=True)
    def test_skips_unverified_recipient(self):
        with self.assertLogs("hub.mail", level="WARNING"):
            self.assertFalse(send("a@example.com", "Hi", "Body"))
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_CONFIGURED=True)
    def test_sends_to_verified_recipient(self):
        user = User.objects.create_user("u", "a@example.com", "pw")
        EmailVerification.objects.create(user=user, email="a@example.com", verified=True)
        self.assertTrue(send("a@example.com", "Hi", "Body"))
        self.assertEqual(len(mail.outbox), 1)
