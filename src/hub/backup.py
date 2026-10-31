"""Full database backup (§17).

``VACUUM INTO`` writes a consistent copy of a live SQLite database, unlike
copying the file. Only SQLite is supported.
"""
import os
import tempfile

from django.db import connection


def create_backup(path):
    """Write a consistent SQLite backup to ``path`` (which must not exist)."""
    if connection.vendor != "sqlite":
        raise RuntimeError("Backup is only supported for SQLite databases.")
    with connection.cursor() as cursor:
        cursor.execute("VACUUM INTO %s", [path])
    return path


def backup_bytes():
    """Return a fresh backup as bytes."""
    fd, path = tempfile.mkstemp(suffix=".sqlite3")
    os.close(fd)
    os.remove(path)  # VACUUM INTO requires the target not to exist
    try:
        create_backup(path)
        with open(path, "rb") as handle:
            return handle.read()
    finally:
        if os.path.exists(path):
            os.remove(path)
