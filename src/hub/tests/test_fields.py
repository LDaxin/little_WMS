from django.core.exceptions import ValidationError
from django.test import TestCase

from storage.models import Storage, StorageType


class SelfForeignKeyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")

    def test_cycle_raises(self):
        a = Storage.objects.create(name="A", typ=self.storage_type)
        b = Storage.objects.create(name="B", typ=self.storage_type, parent=a)
        a.parent = b
        with self.assertRaises(ValidationError):
            a.save()

    def test_depth_raises(self):
        prev = None
        for i in range(7):
            prev = Storage.objects.create(
                name="S%d" % i, typ=self.storage_type, parent=prev
            )
        # 7 ancestors -> allowed
        child = Storage.objects.create(name="X", typ=self.storage_type, parent=prev)
        # 8 ancestors -> rejected
        with self.assertRaises(ValidationError):
            Storage.objects.create(name="Y", typ=self.storage_type, parent=child)
