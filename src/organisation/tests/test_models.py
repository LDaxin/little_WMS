from django.test import TestCase

from article.models import ArticleType
from codeSystem.models import UuidCode
from organisation.models import Organisation
from space.models import Space
from storage.models import StorageType
from tag.models import Tag


class OrganisationModelTest(TestCase):
    def test_default_organisation_exists(self):
        self.assertTrue(Organisation.objects.filter(pk=1).exists())

    def test_str(self):
        organisation = Organisation.objects.create(name="Pfadfinder", slug="pfadfinder")
        self.assertEqual(str(organisation), "Pfadfinder")


class OrganisationFieldTest(TestCase):
    def test_models_default_to_organisation_one(self):
        self.assertEqual(
            ArticleType.objects.create(name="Werkzeug", symbol="WZ").organisation_id, 1
        )
        self.assertEqual(
            StorageType.objects.create(name="Regal", symbol="RG").organisation_id, 1
        )
        self.assertEqual(Tag.objects.create(name="Sommer").organisation_id, 1)
        self.assertEqual(Space.objects.create(prefix="s0").organisation_id, 1)
        self.assertEqual(UuidCode.objects.create(prefix="a0").organisation_id, 1)
