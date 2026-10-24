from django.test import TestCase

from storage.models import Storage, StorageType


def assert_soft_delete_cycle(testcase, obj, model):
    """Characterizes the SoftDeleteObject behaviour for a concrete instance."""
    pk = obj.pk
    obj.delete()
    testcase.assertFalse(model.objects.all().filter(pk=pk).exists())
    testcase.assertTrue(model.objects.all_with_deleted().filter(pk=pk).exists())
    obj.undelete()
    testcase.assertTrue(model.objects.all().filter(pk=pk).exists())


class StorageTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")

    def test_creation(self):
        self.assertEqual(self.storage_type.symbol, "RG")

    def test_name_is_lowercased(self):
        self.assertEqual(self.storage_type.name, "regal")

    def test_code_prefix(self):
        self.assertEqual(self.storage_type.code.prefix, "st")

    def test_str(self):
        self.assertEqual(str(self.storage_type), "regal")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.storage_type, StorageType)


class StorageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def test_creation(self):
        self.assertEqual(self.storage.typ, self.storage_type)

    def test_code_prefix(self):
        self.assertEqual(self.storage.code.prefix, "s0")

    def test_space_is_created(self):
        self.assertIsNotNone(self.storage.space)
        self.assertEqual(self.storage.space.prefix, "s0")

    def test_str_without_parent(self):
        self.assertEqual(str(self.storage), "Regal A")

    def test_str_with_parent(self):
        child = Storage.objects.create(name="Fach 1", typ=self.storage_type, parent=self.storage)
        self.assertEqual(str(child), "Regal A / Fach 1")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.storage, Storage)

    def test_soft_delete_parent_sets_child_parent_null(self):
        parent = Storage.objects.create(name="Regal B", typ=self.storage_type)
        child = Storage.objects.create(name="Fach 1", typ=self.storage_type, parent=parent)
        parent.delete()
        child.refresh_from_db()
        self.assertIsNone(child.parent)
