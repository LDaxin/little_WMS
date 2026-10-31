from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from planning.models import CalendarEntry
from occasion.models import Occasion, OccasionTemplate, OccasionType, Packlist
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

    def test_packlist_search_input_swaps_inner(self):
        # the input must not inherit hx-swap="outerHTML" from the form, or the
        # results container gets replaced and the dropdown only works once
        self.login_superuser()
        response = self.client.get("/occasions/%s/" % self.occasion.pk)
        self.assertContains(response, 'hx-target="#packlistResults" hx-swap="innerHTML"')

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


class OccasionTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.occ_type = OccasionType.objects.create(name="Camp")
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_model_str(self):
        template = OccasionTemplate.objects.create(name="Standard Camp", occasion_type=self.occ_type)
        self.assertEqual(str(template), "Standard Camp")

    def test_save_occasion_as_template(self):
        occasion = make_occasion(self.occ_type)
        Packlist.objects.create(occasion=occasion, article=self.article, quantity=4)
        self.client.post("/occasions/%s/save-template/" % occasion.pk, {"name": "Standard Camp"})
        template = OccasionTemplate.objects.get(name="Standard Camp")
        self.assertEqual(template.occasion_type, self.occ_type)
        self.assertEqual(template.default_packlist, [{"article": self.article.pk, "quantity": 4}])

    def test_create_from_template(self):
        template = OccasionTemplate.objects.create(
            name="Standard Camp",
            occasion_type=self.occ_type,
            default_packlist=[{"article": self.article.pk, "quantity": 4}],
        )
        self.client.post(
            "/occasions/add/",
            {"name": "Summer", "template": template.pk, "start_date": "2026-07-01"},
        )
        occasion = Occasion.objects.get(calendar_entry__title="Summer")
        self.assertEqual(occasion.occasion_type, self.occ_type)
        entry = occasion.packlist.get()
        self.assertEqual(entry.article, self.article)
        self.assertEqual(entry.quantity, 4)

    def test_template_list_and_delete(self):
        template = OccasionTemplate.objects.create(name="Standard Camp", occasion_type=self.occ_type)
        self.assertContains(self.client.get("/occasions/templates/"), "Standard Camp")
        self.client.post("/occasions/templates/%s/delete/" % template.pk)
        template.refresh_from_db()
        self.assertIsNotNone(template.deleted_at)

    def test_template_permission(self):
        user_with("helper", "occasion_view_all")
        self.client.login(username="helper", password="pw")
        response = self.client.post(
            "/occasions/templates/add/", {"name": "X", "type": self.occ_type.pk}
        )
        self.assertEqual(response.status_code, 403)
