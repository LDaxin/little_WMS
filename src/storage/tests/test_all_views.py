from django.contrib.auth.models import User
from django.test import TestCase

from storage.models import Storage, StorageType


def _ids_inside(content, container_id):
    """Ids of elements nested inside ``#<container_id>`` (rough HTML nesting)."""
    from html.parser import HTMLParser

    void = {"input", "br", "img", "meta", "link", "hr"}

    class Nesting(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.found = []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag not in void:
                self.stack.append(attrs.get("id"))
            if attrs.get("id") and container_id in self.stack:
                self.found.append(attrs["id"])

        def handle_endtag(self, tag):
            if tag not in void and self.stack:
                self.stack.pop()

    parser = Nesting()
    parser.feed(content)
    return parser.found


class AllStoragesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        storage_type = StorageType.objects.create(name="room", symbol="RA")
        cls.storage = Storage.objects.create(name="Lager", typ=storage_type)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_storages_all(self):
        self.assertEqual(self.client.get("/storage/").status_code, 200)

    def test_search_all(self):
        response = self.client.get("/storage/search", {"search": "Lager"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lager")

    def test_search_all_links_to_detail(self):
        response = self.client.get("/storage/search", {"search": "Lager"})
        self.assertContains(response, "/storage/room/%s" % self.storage.pk)

    def test_search_all_sorts_by_name(self):
        storage_type = StorageType.objects.get(name="room")
        Storage.objects.create(name="AAA", typ=storage_type)
        content = self.client.get("/storage/search", {"sort": "name"}).content.decode()
        self.assertLess(content.index("AAA"), content.index("Lager"))

    def test_search_all_paginates(self):
        storage_type = StorageType.objects.get(name="room")
        for i in range(51):
            Storage.objects.create(name="S%03d" % i, typ=storage_type)
        response = self.client.get("/storage/search")
        self.assertContains(response, "listControl")
        self.assertContains(response, "page=2")

    def test_search_all_pagination_keeps_sort(self):
        storage_type = StorageType.objects.get(name="room")
        for i in range(51):
            Storage.objects.create(name="S%03d" % i, typ=storage_type)
        response = self.client.get("/storage/search", {"sort": "name"})
        self.assertContains(response, "sort=name")

    def test_select_all_control_present(self):
        response = self.client.get("/storage/room/")
        self.assertContains(response, "selectAllButton")

    def test_bulk_delete_all_matches(self):
        storage_type = StorageType.objects.get(name="room")
        other = Storage.objects.create(name="AAA", typ=storage_type)
        response = self.client.post("/storage/room/del", {"all": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Storage.objects.all().filter(pk=self.storage.pk).exists())
        self.assertFalse(Storage.objects.all().filter(pk=other.pk).exists())

    def test_bulk_delete_all_matches_respects_search(self):
        storage_type = StorageType.objects.get(name="room")
        other = Storage.objects.create(name="AAA", typ=storage_type)
        self.client.post("/storage/room/del", {"all": "1", "search": "Lager"})
        self.assertFalse(Storage.objects.all().filter(pk=self.storage.pk).exists())
        self.assertTrue(Storage.objects.all().filter(pk=other.pk).exists())

    def test_bulk_export_all_matches(self):
        storage_type = StorageType.objects.get(name="room")
        Storage.objects.create(name="AAA", typ=storage_type)
        response = self.client.post("/storage/room/export", {"all": "1"})
        content = response.content.decode("iso-8859-1")
        self.assertIn("Lager", content)
        self.assertIn("AAA", content)

    def test_bulk_qr_all_matches(self):
        storage_type = StorageType.objects.get(name="room")
        Storage.objects.create(name="AAA", typ=storage_type)
        response = self.client.post("/qr/print", {"type": "storage", "typ": "room", "all": "1"})
        self.assertContains(response, "Lager")
        self.assertContains(response, "AAA")

    def test_list_default_applies_on_mobile(self):
        response = self.client.get("/storage/room/")
        self.assertContains(response, 'id="modeInput" name="mode" value=""')
        response = self.client.get("/storage/room/search", HTTP_X_VIEW_MODE="mobile")
        self.assertContains(response, "card-title")

    def test_cards_load_more_at_end_of_list(self):
        storage_type = StorageType.objects.get(name="room")
        for i in range(51):
            Storage.objects.create(name="S%03d" % i, typ=storage_type)
        response = self.client.get("/storage/search", {"mode": "cards"})
        self.assertIn("listControl", _ids_inside(response.content.decode(), "listBody"))
        response = self.client.get("/storage/search", {"mode": "table"})
        self.assertNotIn("listControl", _ids_inside(response.content.decode(), "listBody"))
