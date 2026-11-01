from django.test import TestCase

from location.models import Location


def assert_soft_delete_cycle(testcase, obj, model):
    """Characterizes the SoftDeleteObject behaviour for a concrete instance."""
    pk = obj.pk
    obj.delete()
    testcase.assertFalse(model.objects.all().filter(pk=pk).exists())
    testcase.assertTrue(model.objects.all_with_deleted().filter(pk=pk).exists())
    obj.undelete()
    testcase.assertTrue(model.objects.all().filter(pk=pk).exists())


class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.location = Location.objects.create(
            line1="Invalidenstr. 1",
            postal_code="10115",
            city="Berlin",
            state="Berlin",
            country="DE",
        )

    def test_code_prefix(self):
        self.assertEqual(self.location.code.prefix, "l0")

    def test_coordinates_default_null(self):
        self.assertIsNone(self.location.latitude)
        self.assertIsNone(self.location.longitude)
        self.assertEqual(self.location.plus_code, "")

    def test_str(self):
        self.assertEqual(str(self.location), "Invalidenstr. 1, 10115 Berlin, Berlin, DE")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.location, Location)

    def test_plus_code_derived_on_save(self):
        loc = Location.objects.create(line1="X", latitude=52.52, longitude=13.405)
        self.assertEqual(loc.plus_code, "9F4MGCC4+22")

    def test_plus_code_not_overwritten(self):
        loc = Location.objects.create(
            line1="X", latitude=52.52, longitude=13.405, plus_code="CUSTOM"
        )
        self.assertEqual(loc.plus_code, "CUSTOM")
