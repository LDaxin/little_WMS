import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from article.models import Article, ArticleBase, ArticleImage, ArticleType


def image_file(name="test.jpg", size=(100, 100)):
    buf = BytesIO()
    Image.new("RGB", size, "red").save(buf, format="JPEG")
    return SimpleUploadedFile(name, buf.getvalue(), content_type="image/jpeg")


class ArticleImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

    def setUp(self):
        self.media = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media)
        self.override.enable()

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media, ignore_errors=True)

    def test_thumbnail_generated(self):
        img = ArticleImage.objects.create(article=self.article, image=image_file())
        self.assertTrue(img.thumbnail)
        self.assertTrue(img.thumbnail.storage.exists(img.thumbnail.name))

    def test_primary_image_property(self):
        img = ArticleImage.objects.create(
            article=self.article, image=image_file(), is_primary=True
        )
        self.assertEqual(self.article.primary_image, img)

    def test_delete_removes_files(self):
        img = ArticleImage.objects.create(article=self.article, image=image_file())
        storage = img.image.storage
        name, thumb = img.image.name, img.thumbnail.name
        img.delete()
        self.assertFalse(storage.exists(name))
        self.assertFalse(storage.exists(thumb))


class ArticleImageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.article_base = ArticleBase.objects.create(name="Hammer", pType=cls.article_type)
        cls.article = Article.objects.create(base=cls.article_base)

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
            f"/article/werkzeug/{self.article.pk}/images/add", {"image": image_file()}
        )
        self.assertEqual(response.status_code, 302)
        img = self.article.images.first()
        self.assertIsNotNone(img)
        self.assertTrue(img.is_primary)

    def test_set_primary(self):
        first = ArticleImage.objects.create(
            article=self.article, image=image_file(), is_primary=True
        )
        second = ArticleImage.objects.create(article=self.article, image=image_file())
        self.client.post(
            f"/article/werkzeug/{self.article.pk}/images/{second.pk}/primary"
        )
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertFalse(first.is_primary)
        self.assertTrue(second.is_primary)

    def test_delete_image(self):
        img = ArticleImage.objects.create(article=self.article, image=image_file())
        self.client.post(
            f"/article/werkzeug/{self.article.pk}/images/{img.pk}/delete"
        )
        self.assertFalse(ArticleImage.objects.filter(pk=img.pk).exists())
