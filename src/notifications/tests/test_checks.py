from datetime import date, timedelta

from django.contrib.auth.models import Permission, User
from django.core.management import call_command
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from loans.models import Loan
from notifications.checks import (
    expiry_findings,
    low_stock_findings,
    maintenance_findings,
    return_overdue_findings,
)
from notifications.models import Notification
from organisation.models import Organisation, Role, UserProfile
from planning.models import CalendarEntry


class ChecksTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type, organisation=cls.org)

    def test_expiry_finding(self):
        Article.objects.create(
            base=self.base, organisation=self.org, ablaufdatum=date.today() + timedelta(days=3)
        )
        findings = list(expiry_findings(self.org))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].trigger_type, "expiry_date_reached")

    def test_maintenance_finding(self):
        CalendarEntry.objects.create(
            entry_type="maintenance", title="Sharpen", start_date=date.today(), organisation=self.org
        )
        findings = list(maintenance_findings(self.org))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].trigger_type, "maintenance_due")

    def test_low_stock_finding(self):
        self.base.mindestbestand = 5
        self.base.save()
        article = Article.objects.create(base=self.base, organisation=self.org)
        Stock.objects.create(article=article, menge=2)
        findings = list(low_stock_findings(self.org))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].trigger_type, "minimum_stock_undercut")


class ReturnOverdueTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type, organisation=cls.org)
        cls.article = Article.objects.create(base=cls.base, organisation=cls.org)

    def _loan(self, status="active", direction="out"):
        entry = CalendarEntry.objects.create(
            entry_type="loan", title="Loan", organisation=self.org, article=self.article,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() - timedelta(days=1),
        )
        return Loan.objects.create(
            article=self.article, calendar_entry=entry, direction=direction,
            party_name="Anna", organisation=self.org, status=status,
        )

    def test_overdue_loan(self):
        self._loan()
        findings = list(return_overdue_findings(self.org))
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].trigger_type, "return_overdue")

    def test_returned_loan_no_finding(self):
        self._loan(status="returned")
        self.assertEqual(list(return_overdue_findings(self.org)), [])


class CommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tool", symbol="WZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type, organisation=cls.org)

    def setUp(self):
        role = Role.objects.create(organisation=self.org, name="R")
        role.permissions.set(Permission.objects.filter(codename="article_view_all"))
        self.user = User.objects.create_user("u", password="pw")
        UserProfile.objects.create(user=self.user, organisation=self.org, role=role)

    def test_command_creates_and_dedupes(self):
        Article.objects.create(
            base=self.base, organisation=self.org, ablaufdatum=date.today() + timedelta(days=3)
        )
        call_command("check_notifications")
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 1)
        call_command("check_notifications")
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 1)

    def test_command_creates_and_dedupes_overdue(self):
        entry = CalendarEntry.objects.create(
            entry_type="loan", title="Loan", organisation=self.org,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() - timedelta(days=1),
        )
        article = Article.objects.create(base=self.base, organisation=self.org)
        Loan.objects.create(
            article=article, calendar_entry=entry, party_name="Anna", organisation=self.org
        )
        call_command("check_notifications")
        self.assertEqual(
            Notification.objects.filter(user=self.user, trigger_type="return_overdue").count(), 1
        )
        call_command("check_notifications")
        self.assertEqual(
            Notification.objects.filter(user=self.user, trigger_type="return_overdue").count(), 1
        )
