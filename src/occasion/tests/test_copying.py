from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from occasion.models import Occasion, OccasionType, Packlist
from organisation.models import Role, UserProfile
from planning.models import CalendarEntry


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class OccasionCopyingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.occ_type = OccasionType.objects.create(name="Camp")
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def _occasion(self):
        entry = CalendarEntry.objects.create(
            title="Sommerlager", start_date="2026-07-01", end_date="2026-07-14"
        )
        occasion = Occasion.objects.create(
            calendar_entry=entry, occasion_type=self.occ_type, participant_count=30
        )
        Packlist.objects.create(occasion=occasion, article=self.article, quantity=4)
        return occasion

    def test_duplicate_copies_type_and_packlist(self):
        occasion = self._occasion()
        self.client.post("/occasions/%s/duplicate/" % occasion.pk, {"shift_days": "0"})
        copy = Occasion.objects.exclude(pk=occasion.pk).get()
        self.assertEqual(copy.occasion_type, self.occ_type)
        self.assertEqual(copy.participant_count, 30)
        self.assertEqual(copy.packlist.get().quantity, 4)
        self.assertEqual(copy.calendar_entry.title, "Sommerlager (copy)")

    def test_duplicate_shifts_dates(self):
        occasion = self._occasion()
        self.client.post("/occasions/%s/duplicate/" % occasion.pk, {"shift_days": "364"})
        copy = Occasion.objects.exclude(pk=occasion.pk).get()
        self.assertEqual(str(copy.calendar_entry.start_date), "2027-06-30")
        self.assertEqual(str(copy.calendar_entry.end_date), "2027-07-13")

    def test_duplicate_permission(self):
        occasion = self._occasion()
        user_with("helper", "occasion_view_all")
        self.client.login(username="helper", password="pw")
        response = self.client.post(
            "/occasions/%s/duplicate/" % occasion.pk, {"shift_days": "0"}
        )
        self.assertEqual(response.status_code, 403)
