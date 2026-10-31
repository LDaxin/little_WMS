from datetime import date, timedelta

from django.contrib.auth.models import Permission, User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings

from article.models import Article, ArticleBase, ArticleType
from notifications.models import Notification, NotificationRule
from organisation.models import EmailVerification, Organisation, Role, UserProfile


class RuleRecipientsTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        self.role = Role.objects.create(organisation=self.org, name="R")
        self.role_user = User.objects.create_user("roleuser", "r@example.com", "pw")
        UserProfile.objects.create(user=self.role_user, organisation=self.org, role=self.role)
        self.direct_user = User.objects.create_user("direct", "d@example.com", "pw")
        UserProfile.objects.create(user=self.direct_user, organisation=self.org)

    def test_recipients_union(self):
        rule = NotificationRule.objects.create(
            organisation=self.org, trigger_type="expiry_date_reached"
        )
        rule.notify_roles.add(self.role)
        rule.notify_users.add(self.direct_user)
        self.assertEqual(set(rule.recipients()), {self.role_user, self.direct_user})


class RuleCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type, organisation=cls.org)

    def setUp(self):
        self.user = User.objects.create_user("u", "u@example.com", "pw")
        UserProfile.objects.create(user=self.user, organisation=self.org)

    def _expiring_article(self):
        Article.objects.create(
            base=self.base, organisation=self.org, ablaufdatum=date.today() + timedelta(days=3)
        )

    def test_rule_in_app(self):
        self._expiring_article()
        rule = NotificationRule.objects.create(
            organisation=self.org, trigger_type="expiry_date_reached",
            channel_in_app=True, channel_email=False,
        )
        rule.notify_users.add(self.user)
        call_command("check_notifications")
        self.assertTrue(
            Notification.objects.filter(user=self.user, trigger_type="expiry_date_reached").exists()
        )

    @override_settings(EMAIL_CONFIGURED=True)
    def test_rule_email(self):
        self._expiring_article()
        EmailVerification.objects.create(user=self.user, email="u@example.com", verified=True)
        rule = NotificationRule.objects.create(
            organisation=self.org, trigger_type="expiry_date_reached",
            channel_in_app=True, channel_email=True,
        )
        rule.notify_users.add(self.user)
        call_command("check_notifications")
        self.assertEqual(len(mail.outbox), 1)

    def test_no_rule_default(self):
        self._expiring_article()
        role = Role.objects.create(organisation=self.org, name="R")
        role.permissions.set(Permission.objects.filter(codename="article_view_all"))
        UserProfile.objects.filter(user=self.user).update(role=role)
        call_command("check_notifications")
        self.assertTrue(Notification.objects.filter(user=self.user).exists())


class RulesViewTest(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="A", slug="a")
        role = Role.objects.create(organisation=self.org, name="R")
        role.permissions.set(Permission.objects.filter(codename="notification_manage_rules_all"))
        self.user = User.objects.create_user("u", password="pw")
        UserProfile.objects.create(user=self.user, organisation=self.org, role=role)
        self.client.login(username="u", password="pw")

    def test_page_returns_200(self):
        self.assertEqual(self.client.get("/notifications/rules/").status_code, 200)

    def test_add_rule(self):
        self.client.post("/notifications/rules/add/", {
            "trigger_type": "expiry_date_reached", "active": "on", "channel_in_app": "on",
        })
        self.assertTrue(NotificationRule.objects.filter(organisation=self.org).exists())

    def test_requires_permission(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/notifications/rules/").status_code, 403)
