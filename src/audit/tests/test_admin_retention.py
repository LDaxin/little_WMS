from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from article.models import Article, ArticleBase, ArticleType
from audit.models import AuditLog
from audit.services import log
from organisation.models import Organisation


class RetentionCutoffTest(TestCase):
    def test_forever_returns_none(self):
        org = Organisation.objects.create(name="Org", slug="org")
        self.assertIsNone(org.retention_cutoff())

    def test_days_returns_cutoff(self):
        org = Organisation.objects.create(name="Org", slug="org", log_retention_days=30)
        cutoff = org.retention_cutoff()
        self.assertAlmostEqual(
            (timezone.now() - cutoff).total_seconds(), 30 * 86400, delta=60
        )


class PurgeAuditLogTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # entries are logged against the default organisation (pk=1)
        cls.org = Organisation.objects.get(pk=1)
        cls.org.log_retention_days = 30
        cls.org.save()
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def make_entry(self, age_days):
        entry = log("created", self.article)
        AuditLog.objects.filter(pk=entry.pk).update(
            timestamp=timezone.now() - timedelta(days=age_days)
        )
        return entry

    def test_purge_deletes_old_keeps_new(self):
        old = self.make_entry(40)
        new = self.make_entry(1)
        call_command("purge_audit_log")
        self.assertFalse(AuditLog.objects.filter(pk=old.pk).exists())
        self.assertTrue(AuditLog.objects.filter(pk=new.pk).exists())

    def test_dry_run_keeps_entries(self):
        old = self.make_entry(40)
        call_command("purge_audit_log", "--dry-run")
        self.assertTrue(AuditLog.objects.filter(pk=old.pk).exists())

    def test_forever_keeps_entries(self):
        self.org.log_retention_days = None
        self.org.save()
        old = self.make_entry(4000)
        call_command("purge_audit_log")
        self.assertTrue(AuditLog.objects.filter(pk=old.pk).exists())


class AuditAdminTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "a@b.c", "pw")
        self.client.login(username="admin", password="pw")

    def test_changelist_loads(self):
        response = self.client.get("/admin/audit/auditlog/")
        self.assertEqual(response.status_code, 200)

    def test_add_is_blocked(self):
        response = self.client.get("/admin/audit/auditlog/add/")
        self.assertEqual(response.status_code, 403)
