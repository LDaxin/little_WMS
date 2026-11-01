import json
import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from storage.models import FloorPlan, FloorPlanArea, Storage, StorageType


def image_file(name="plan.jpg", size=(200, 150)):
    buf = BytesIO()
    Image.new("RGB", size, "white").save(buf, format="JPEG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/jpeg")


class FloorPlanModelTest(TestCase):
    def setUp(self):
        self.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        self.storage = Storage.objects.create(name="Regal A", typ=self.storage_type)

    def test_plan_created_for_storage(self):
        plan = FloorPlan.objects.create(storage=self.storage)
        self.assertEqual(FloorPlan.objects.get(storage=self.storage), plan)

    def test_area_shape(self):
        plan = FloorPlan.objects.create(storage=self.storage)
        area = FloorPlanArea.objects.create(
            floor_plan=plan,
            storage=self.storage,
            shape={"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4},
        )
        self.assertEqual(area.shape["w"], 0.3)
        self.assertEqual(area.storage, self.storage)


class FloorPlanViewTest(TestCase):
    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()
        self.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        self.storage = Storage.objects.create(name="Regal A", typ=self.storage_type)
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media, ignore_errors=True)

    def _upload(self, name="plan.jpg"):
        return self.client.post(
            f"/storage/regal/{self.storage.pk}/plan/upload", {"image": image_file(name)}
        )

    def _save_areas(self, areas):
        return self.client.post(
            f"/storage/regal/{self.storage.pk}/plan/areas", {"areas": json.dumps(areas)}
        )

    def test_upload_plan(self):
        response = self._upload()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FloorPlan.objects.get(storage=self.storage).image)

    def test_upload_resizes_large_image(self):
        self.client.post(
            f"/storage/regal/{self.storage.pk}/plan/upload",
            {"image": image_file("big.jpg", size=(3000, 2000))},
        )
        plan = FloorPlan.objects.get(storage=self.storage)
        self.assertLessEqual(max(plan.image.width, plan.image.height), 2000)

    def test_save_areas(self):
        self._save_areas([
            {"x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2, "storage": self.storage.pk, "label": "A", "color": "#0d6efd"}
        ])
        area = FloorPlan.objects.get(storage=self.storage).areas.first()
        self.assertIsNotNone(area)
        self.assertEqual(area.storage, self.storage)
        self.assertEqual(area.label, "A")

    def test_replace_plan_keeps_areas(self):
        self._upload()
        self._save_areas([
            {"x": 0, "y": 0, "w": 0.5, "h": 0.5, "storage": "", "label": "", "color": "#0d6efd"}
        ])
        self._upload("plan2.jpg")
        self.assertEqual(FloorPlan.objects.get(storage=self.storage).areas.count(), 1)

    def test_plan_page_renders(self):
        self._upload()
        response = self.client.get(f"/storage/regal/{self.storage.pk}/plan")
        self.assertEqual(response.status_code, 200)

    def test_plan_shows_areas(self):
        """An area linked to a storage without a plan opens that storage."""
        child = Storage.objects.create(name="Regal B", typ=self.storage_type)
        self._upload()
        self._save_areas([
            {"x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2, "storage": child.pk, "label": "A", "color": "#0d6efd"}
        ])
        response = self.client.get(f"/storage/regal/{self.storage.pk}/plan")
        self.assertContains(response, 'fill="#0d6efd33"')
        self.assertContains(response, f'data-href="/storage/regal/{child.pk}"')

    def test_plan_area_opens_target_plan_when_it_has_one(self):
        """An area whose storage has its own plan opens that plan."""
        child = Storage.objects.create(name="Regal B", typ=self.storage_type)
        FloorPlan.objects.create(storage=child, image=image_file("child.jpg"))
        self._upload()
        self._save_areas([
            {"x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2, "storage": child.pk, "label": "A", "color": "#0d6efd"}
        ])
        response = self.client.get(f"/storage/regal/{self.storage.pk}/plan")
        self.assertContains(response, f'data-href="/storage/regal/{child.pk}/plan"')

    def test_plan_links_back_to_storage(self):
        self._upload()
        response = self.client.get(f"/storage/regal/{self.storage.pk}/plan")
        self.assertContains(response, f'href="/storage/regal/{self.storage.pk}"')

    def test_plan_areas_keep_dot_in_german_locale(self):
        """Regression KI-024: a German decimal comma must not break the SVG coords."""
        self._upload()
        self._save_areas([
            {"x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2, "storage": self.storage.pk, "label": "A", "color": "#0d6efd"}
        ])
        response = self.client.get(
            f"/storage/regal/{self.storage.pk}/plan", HTTP_ACCEPT_LANGUAGE="de"
        )
        self.assertContains(response, "Übersicht")  # German locale is active
        self.assertContains(response, 'x="20')  # dot-formatted coordinate
        self.assertNotContains(response, 'x="20,')  # no German decimal comma

    def test_highlight(self):
        self._upload()
        self._save_areas([
            {"x": 0, "y": 0, "w": 0.5, "h": 0.5, "storage": self.storage.pk, "label": "", "color": "#0d6efd"}
        ])
        response = self.client.get(
            f"/storage/regal/{self.storage.pk}/plan?highlight={self.storage.pk}"
        )
        self.assertContains(response, 'stroke-width="4"')
