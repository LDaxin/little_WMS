from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings

from hub.mail import is_subscribed, send, set_subscription
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


class EmailPreferenceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", "u@example.com", "pw")

    def test_default_subscribed(self):
        self.assertTrue(is_subscribed(self.user, "notifications"))

    def test_opt_out_is_per_category(self):
        set_subscription(self.user, "notifications", False)
        self.assertFalse(is_subscribed(self.user, "notifications"))
        self.assertTrue(is_subscribed(self.user, "invitations"))

    @override_settings(EMAIL_CONFIGURED=True)
    def test_send_skips_opted_out_category(self):
        set_subscription(self.user, "notifications", False)
        with self.assertLogs("hub.mail", level="WARNING"):
            self.assertFalse(send("u@example.com", "Hi", "Body",
                                  require_verified=False, category="notifications"))
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_CONFIGURED=True)
    def test_send_subscribed_category(self):
        self.assertTrue(send("u@example.com", "Hi", "Body",
                             require_verified=False, category="notifications"))
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(EMAIL_CONFIGURED=True)
    def test_send_to_non_user_ignores_category(self):
        self.assertTrue(send("stranger@example.com", "Hi", "Body",
                             require_verified=False, category="invitations"))
        self.assertEqual(len(mail.outbox), 1)
