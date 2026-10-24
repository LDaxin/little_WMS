from django.test import TestCase

from tag.models import Tag


def assert_soft_delete_cycle(testcase, obj, model):
    """Characterizes the SoftDeleteObject behaviour for a concrete instance."""
    pk = obj.pk
    obj.delete()
    testcase.assertFalse(model.objects.all().filter(pk=pk).exists())
    testcase.assertTrue(model.objects.all_with_deleted().filter(pk=pk).exists())
    obj.undelete()
    testcase.assertTrue(model.objects.all().filter(pk=pk).exists())


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tag = Tag.objects.create(name="Werkzeug")

    def test_code_prefix(self):
        self.assertEqual(self.tag.code.prefix, "t0")

    def test_str_without_parent(self):
        self.assertEqual(str(self.tag), "Werkzeug")

    def test_str_with_parent(self):
        child = Tag.objects.create(name="Hammer", parent=self.tag)
        self.assertEqual(str(child), "Werkzeug/Hammer")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.tag, Tag)
