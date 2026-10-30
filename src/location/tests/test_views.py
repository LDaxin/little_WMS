from django.contrib.auth.models import User
from django.test import TestCase

from location.models import Location


class LocationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.location = Location.objects.create(
            line1="Invalidenstr. 1",
            postal_code="10115",
            city="Berlin",
            state="Berlin",
            country="DE",
        )

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
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
                "line1": "Marienplatz 1",
                "line2": "",
                "postal_code": "80331",
                "city": "Muenchen",
                "state": "Bayern",
                "country": "DE",
                "latitude": "",
                "longitude": "",
                "plus_code": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Location.objects.filter(city="Muenchen").exists())

    def test_update_location(self):
        response = self.client.post(
            f"/location/{self.location.pk}/update",
            {
                "line1": "Moenckebergstr. 1",
                "line2": "",
                "postal_code": "20095",
                "city": "Hamburg",
                "state": "Hamburg",
                "country": "DE",
                "latitude": "",
                "longitude": "",
                "plus_code": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.location.refresh_from_db()
        self.assertEqual(self.location.city, "Hamburg")

    def test_delete_location(self):
        response = self.client.post(
            "/location/del", {f"_{self.location.pk}": str(self.location.pk)}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Location.objects.all().filter(pk=self.location.pk).exists())

    def test_search_with_term(self):
        response = self.client.get("/location/search?search=Berlin")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Berlin")
