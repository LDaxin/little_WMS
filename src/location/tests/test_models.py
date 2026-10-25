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
            traditionalLand="Deutschland",
            traditionalCountry="DE",
            traditionalCity="Berlin",
            traditionalZipcode="10115",
            traditionalStreet="Invalidenstr.",
            traditionalStreetNumber="1",
        )

    def test_code_prefix(self):
        self.assertEqual(self.location.code.prefix, "l0")

    def test_modern_fields_default_null(self):
        self.assertIsNone(self.location.modernCoordinatesLongitude)
        self.assertIsNone(self.location.modernCoordinatesLatitude)
        self.assertIsNone(self.location.modernWhat3Words)
        self.assertIsNone(self.location.modernWhat3WordsLang)

    def test_str(self):
        self.assertEqual(str(self.location), "Deutschland DE 10115 Invalidenstr. 1")

    def test_soft_delete_and_undelete(self):
        assert_soft_delete_cycle(self, self.location, Location)
