from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from occasion.models import CalendarEntry, Occasion, OccasionType, Packlist
from organisation.models import Role, UserProfile


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


def make_occasion(occ_type, title="Summer"):
    entry = CalendarEntry.objects.create(title=title, start_date="2026-07-01")
    return Occasion.objects.create(calendar_entry=entry, occasion_type=occ_type)


class OccasionModelTest(TestCase):
    def test_defaults_and_str(self):
        occ_type = OccasionType.objects.create(name="Camp")
        occasion = make_occasion(occ_type)
        self.assertEqual(occasion.organisation_id, 1)
        self.assertEqual(str(occasion), "Summer")


class OccasionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.occ_type = OccasionType.objects.create(name="Camp")

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_add_and_list(self):
        self.client.post(
            "/occasions/add/",
            {"name": "Summer", "type": self.occ_type.pk, "start_date": "2026-07-01"},
        )
        self.assertTrue(Occasion.objects.filter(calendar_entry__title="Summer").exists())
        self.assertContains(self.client.get("/occasions/"), "Summer")

    def test_add_without_location(self):
        # the empty location select used to crash with ValueError
        response = self.client.post(
            "/occasions/add/",
            {"name": "NoLoc", "type": self.occ_type.pk, "start_date": "2026-07-01", "location": ""},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Occasion.objects.filter(calendar_entry__title="NoLoc").exists())

    def test_detail_and_update(self):
        occasion = make_occasion(self.occ_type)
        self.assertEqual(self.client.get("/occasions/%s/" % occasion.pk).status_code, 200)
        self.client.post(
            "/occasions/%s/update/" % occasion.pk,
            {"name": "Renamed", "start_date": "2026-07-02"},
        )
        occasion.refresh_from_db()
        self.assertEqual(occasion.calendar_entry.title, "Renamed")

    def test_delete(self):
        occasion = make_occasion(self.occ_type)
        self.client.post("/occasions/%s/delete/" % occasion.pk)
        self.assertFalse(Occasion.objects.filter(pk=occasion.pk).exists())

    def test_requires_permission(self):
        User.objects.create_user("nobody", password="pw")
        self.client.login(username="nobody", password="pw")
        self.assertEqual(self.client.get("/occasions/").status_code, 403)


class PacklistTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.occ_type = OccasionType.objects.create(name="Camp")
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        self.occasion = make_occasion(self.occ_type)

    def login_superuser(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_packlist_has_qr_scanner(self):
        self.login_superuser()
        response = self.client.get("/occasions/%s/" % self.occasion.pk)
        self.assertContains(response, "QRButtonpacklistCode")
        self.assertContains(response, "scannerDivpacklistCode")

    def test_packlist_search_by_name(self):
        self.login_superuser()
        response = self.client.get(
            "/occasions/%s/packlist/search/" % self.occasion.pk, {"code": "Hammer"}
        )
        self.assertContains(response, self.article.code.code)

    def test_packlist_permission(self):
        user_with("helper", "occasion_view_all")
        self.client.login(username="helper", password="pw")
        response = self.client.post(
            "/occasions/%s/packlist/add/" % self.occasion.pk,
            {"code": self.article.code.code},
        )
        self.assertEqual(response.status_code, 403)

    def test_add_status_remove(self):
        self.login_superuser()
        self.client.post(
            "/occasions/%s/packlist/add/" % self.occasion.pk,
            {"code": self.article.code.code, "quantity": "3"},
        )
        entry = Packlist.objects.get(occasion=self.occasion)
        self.assertEqual(entry.quantity, 3)
        self.assertEqual(entry.status, "needed")

        self.client.post(
            "/occasions/%s/packlist/%s/status/" % (self.occasion.pk, entry.pk),
            {"status": "reserved"},
        )
        entry.refresh_from_db()
        self.assertEqual(entry.status, "reserved")

        self.client.post("/occasions/%s/packlist/%s/remove/" % (self.occasion.pk, entry.pk))
        self.assertFalse(Packlist.objects.filter(pk=entry.pk).exists())
