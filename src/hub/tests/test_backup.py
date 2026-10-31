import os
import sqlite3
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase

from hub.backup import create_backup


def _temp_path():
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    os.remove(path)
    return path


class BackupServiceTest(TransactionTestCase):
    # VACUUM cannot run inside a transaction, so these use TransactionTestCase.

    def test_create_backup_is_valid_sqlite(self):
        path = _temp_path()
        try:
            create_backup(path)
            connection = sqlite3.connect(path)
            connection.execute("SELECT 1")
            connection.close()
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_command_writes_backup(self):
        path = _temp_path()
        try:
            call_command("backup", path)
            self.assertTrue(os.path.getsize(path) > 0)
        finally:
            if os.path.exists(path):
                os.remove(path)


class BackupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("root", "root@example.com", "pw")
        self.client.login(username="root", password="pw")

    @patch("hub.backup.backup_bytes", return_value=b"data")
    def test_download(self, mock_backup):
        response = self.client.get("/server-settings/backup/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment", response["Content-Disposition"])

    def test_requires_superuser(self):
        User.objects.create_user("other", password="pw")
        self.client.login(username="other", password="pw")
        self.assertEqual(self.client.get("/server-settings/backup/").status_code, 403)
