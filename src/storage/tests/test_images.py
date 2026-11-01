import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from storage.models import Storage, StorageImage, StorageType


def image_file(name="test.jpg", size=(100, 100)):
    buf = BytesIO()
    Image.new("RGB", size, "blue").save(buf, format="JPEG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/jpeg")


class StorageImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media, ignore_errors=True)

    def test_thumbnail_generated(self):
        img = StorageImage.objects.create(storage=self.storage, image=image_file())
        self.assertTrue(img.thumbnail.storage.exists(img.thumbnail.name))

    def test_primary_image_property(self):
        img = StorageImage.objects.create(
            storage=self.storage, image=image_file(), is_primary=True
        )
        self.assertEqual(self.storage.primary_image, img)


class StorageImageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.storage_type = StorageType.objects.create(name="Regal", symbol="RG")
        cls.storage = Storage.objects.create(name="Regal A", typ=cls.storage_type)

    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()
        self.user = User.objects.create_superuser("tester", "tester@example.com", "pw")
        self.client.login(username="tester", password="pw")

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media, ignore_errors=True)

    def test_upload_first_image_is_primary(self):
        response = self.client.post(
            f"/storage/regal/{self.storage.pk}/images/add", {"image": image_file()}
        )
        self.assertEqual(response.status_code, 302)
        img = self.storage.images.first()
        self.assertIsNotNone(img)
        self.assertTrue(img.is_primary)

    def test_delete_image(self):
        img = StorageImage.objects.create(storage=self.storage, image=image_file())
        self.client.post(
            f"/storage/regal/{self.storage.pk}/images/{img.pk}/delete"
        )
        self.assertFalse(StorageImage.objects.filter(pk=img.pk).exists())
