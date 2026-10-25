from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.test import TestCase

from location.models import Location


class LocationViewTest(TestCase):
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

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pw")
        self.client.login(username="tester", password="pw")

    def test_pages_return_200(self):
        urls = [
            "/location/",
            f"/location/{self.location.pk}",
            f"/location/{self.location.pk}/i",
            "/location/search?search=",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get("/location/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_add_location(self):
        response = self.client.post(
            "/location/add",
            {
                "traditionalLand": "Deutschland",
                "traditionalCountry": "BY",
                "traditionalCity": "Muenchen",
                "traditionalZipcode": "80331",
                "traditionalStreet": "Marienplatz",
                "traditionalStreetNumber": "1",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Location.objects.filter(traditionalCity="Muenchen").exists())

    def test_update_location(self):
        response = self.client.post(
            f"/location/{self.location.pk}/update",
            {
                "traditionalLand": "Deutschland",
                "traditionalCountry": "DE",
                "traditionalCity": "Hamburg",
                "traditionalZipcode": "20095",
                "traditionalStreet": "Moenckebergstr.",
                "traditionalStreetNumber": "1",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.location.refresh_from_db()
        self.assertEqual(self.location.traditionalCity, "Hamburg")

    def test_delete_location(self):
        response = self.client.post(
            "/location/del", {f"_{self.location.pk}": str(self.location.pk)}
        )
        self.assertEqual(response.status_code, 200)
        # SoftDeleteManager.filter(pk=...) intentionally includes soft-deleted
        # rows, so the filtered queryset is used here (see softdelete/models.py).
        self.assertFalse(Location.objects.all().filter(pk=self.location.pk).exists())

    def test_search_with_term_raises_field_error(self):
        # Characterization: Location has no `name` field, so a non-empty search
        # term makes the view raise FieldError (HTTP 500).
        with self.assertRaises(FieldError), self.assertLogs("django.request", level="ERROR"):
            self.client.get("/location/search?search=Berlin")
