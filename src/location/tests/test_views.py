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

    def test_map_requires_login(self):
        self.client.logout()
        response = self.client.get("/location/map")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_map_shows_locations_with_coordinates(self):
        Location.objects.create(line1="Mapped", latitude=52.52, longitude=13.405)
        response = self.client.get("/location/map")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "52.52")
        self.assertContains(response, "13.405")

    def test_map_omits_locations_without_coordinates(self):
        response = self.client.get("/location/map")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Invalidenstr. 1")

    def test_add_location_from_plus_code(self):
        response = self.client.post(
            "/location/add",
            {
                "line1": "Plus",
                "line2": "",
                "postal_code": "",
                "city": "",
                "state": "",
                "country": "",
                "latitude": "",
                "longitude": "",
                "plus_code": "9F4MGCC4+22",
            },
        )
        self.assertEqual(response.status_code, 200)
        loc = Location.objects.get(line1="Plus")
        self.assertAlmostEqual(loc.latitude, 52.5200625, places=3)
        self.assertAlmostEqual(loc.longitude, 13.4050625, places=3)

    def _linked_location(self):
        from storage.models import Storage, StorageType
        from occasion.models import Occasion, OccasionType
        from planning.models import CalendarEntry

        loc = Location.objects.create(line1="Camp", latitude=52.52, longitude=13.405)
        stype = StorageType.objects.create(name="room", symbol="RA")
        Storage.objects.create(name="Lager Nord", typ=stype, location=loc)
        otype = OccasionType.objects.create(name="Camp")
        entry = CalendarEntry.objects.create(title="Summer Camp", start_date="2026-07-01")
        Occasion.objects.create(calendar_entry=entry, occasion_type=otype, location=loc)
        return loc

    def test_map_popup_lists_linked_objects(self):
        self._linked_location()
        response = self.client.get("/location/map")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lager Nord")
        self.assertContains(response, "Summer Camp")

    def test_map_popup_links_to_floor_plan(self):
        import shutil
        import tempfile
        from io import BytesIO

        from django.core.files.uploadedfile import SimpleUploadedFile
        from django.test import override_settings
        from PIL import Image

        from storage.models import FloorPlan, Storage, StorageType

        media = tempfile.mkdtemp()
        try:
            with override_settings(MEDIA_ROOT=media):
                loc = Location.objects.create(line1="Camp", latitude=52.52, longitude=13.405)
                stype = StorageType.objects.create(name="room", symbol="RA")
                storage = Storage.objects.create(name="Lager Nord", typ=stype, location=loc)
                buf = BytesIO()
                Image.new("RGB", (20, 20), "white").save(buf, format="JPEG")
                FloorPlan.objects.create(
                    storage=storage,
                    image=SimpleUploadedFile("p.jpg", buf.getvalue(), content_type="image/jpeg"),
                )
                response = self.client.get("/location/map")
                self.assertContains(response, f"/storage/room/{storage.pk}/plan")
        finally:
            shutil.rmtree(media, ignore_errors=True)

    def test_location_detail_shows_linked_objects(self):
        loc = self._linked_location()
        response = self.client.get(f"/location/{loc.pk}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lager Nord")
        self.assertContains(response, "Summer Camp")

    def test_location_detail_has_map_picker(self):
        response = self.client.get(f"/location/{self.location.pk}/i")
        self.assertContains(response, "locationPicker")

    def test_location_list_has_add_button(self):
        response = self.client.get("/location/")
        self.assertContains(response, "modalButtonAdd")

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
