from django.contrib.auth.models import User
from django.test import TestCase

from storage.models import Storage, StorageType


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
