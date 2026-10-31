from django.contrib.auth.models import Permission, User
from django.core import mail
from django.test import TestCase, override_settings

from hub.mail import set_subscription
from notifications.models import Notification
from notifications.services import notify, notify_roles
from organisation.models import EmailVerification, Organisation, Role, UserProfile


class NotificationServiceTest(TestCase):
    def test_notify_creates_unread(self):
        user = User.objects.create_user("u", password="pw")
        notify(user, "Hello", message="World", link="/x/", trigger_type="test")
        notification = Notification.objects.get(user=user)
        self.assertEqual(notification.title, "Hello")
        self.assertEqual(notification.message, "World")
        self.assertFalse(notification.is_read)

    def test_notify_roles(self):
        organisation = Organisation.objects.create(name="A", slug="a")
        role = Role.objects.create(organisation=organisation, name="R")
        role.permissions.set(Permission.objects.filter(codename="article_view_all"))
        user = User.objects.create_user("u", password="pw")
        UserProfile.objects.create(user=user, organisation=organisation, role=role)
        notify_roles(organisation, "article_view_all", "Hi")
        self.assertTrue(Notification.objects.filter(user=user).exists())


class NotificationCenterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_page_lists(self):
        notify(self.user, "Hello")
        self.assertContains(self.client.get("/notifications/"), "Hello")

    def test_mark_read(self):
        notification = notify(self.user, "Hello")
        self.client.post("/notifications/%s/read/" % notification.pk)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_all_read(self):
        notify(self.user, "A")
        notify(self.user, "B")
        self.client.post("/notifications/read-all/")
        self.assertFalse(Notification.objects.filter(user=self.user, is_read=False).exists())

    def test_permission(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/notifications/").status_code, 403)


class NotificationEmailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("u", "u@example.com", "pw")

    @override_settings(EMAIL_CONFIGURED=True)
    def test_notify_sends_email_when_verified(self):
        EmailVerification.objects.create(user=self.user, email="u@example.com", verified=True)
        notify(self.user, "Hello", message="World", link="/x/")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Hello")

    @override_settings(EMAIL_CONFIGURED=True)
    def test_notify_skips_unverified(self):
        notify(self.user, "Hello")
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_CONFIGURED=True)
    def test_notify_skips_opted_out(self):
        EmailVerification.objects.create(user=self.user, email="u@example.com", verified=True)
        set_subscription(self.user, "notifications", False)
        notify(self.user, "Hello")
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(Notification.objects.filter(user=self.user).exists())
