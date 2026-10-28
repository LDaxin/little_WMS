from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from article.models import ArticleType
from organisation.current import (
    clear_current_organisation,
    get_current_organisation,
    set_current_organisation,
)
from organisation.middleware import ActiveOrganisationMiddleware
from organisation.models import Organisation, UserProfile


class ScopingTest(TestCase):
    def setUp(self):
        self.org_a = Organisation.objects.create(name="A", slug="a")
        self.org_b = Organisation.objects.create(name="B", slug="b")

    def tearDown(self):
        clear_current_organisation()

    def test_reads_are_filtered(self):
        set_current_organisation(self.org_a)
        ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        set_current_organisation(self.org_b)
        ArticleType.objects.create(name="Zelt", symbol="ZT")

        set_current_organisation(self.org_a)
        self.assertEqual(set(ArticleType.objects.values_list("name", flat=True)), {"werkzeug"})

    def test_without_thread_local_all_visible(self):
        set_current_organisation(self.org_a)
        ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        set_current_organisation(self.org_b)
        ArticleType.objects.create(name="Zelt", symbol="ZT")
        clear_current_organisation()
        self.assertEqual(ArticleType.objects.count(), 2)

    def test_create_defaults_to_active_org(self):
        set_current_organisation(self.org_b)
        article_type = ArticleType.objects.create(name="Zelt", symbol="ZT")
        self.assertEqual(article_type.organisation, self.org_b)

    def test_soft_delete_still_filters(self):
        set_current_organisation(self.org_a)
        article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        article_type.delete()
        self.assertEqual(ArticleType.objects.count(), 0)


class MiddlewareTest(TestCase):
    def test_sets_and_clears_current_organisation(self):
        user = User.objects.create_user("tester", password="pw")
        org = Organisation.objects.create(name="A", slug="a")
        UserProfile.objects.create(user=user, organisation=org)

        request = RequestFactory().get("/")
        request.user = user
        request.session = {}
        seen = {}

        def get_response(req):
            seen["org"] = get_current_organisation()
            return "ok"

        ActiveOrganisationMiddleware(get_response)(request)
        self.assertEqual(seen["org"], org)
        self.assertIsNone(get_current_organisation())

    def test_admin_is_skipped(self):
        user = User.objects.create_user("tester", password="pw")

        request = RequestFactory().get("/admin/")
        request.user = user
        seen = {}

        def get_response(req):
            seen["org"] = get_current_organisation()
            return "ok"

        ActiveOrganisationMiddleware(get_response)(request)
        self.assertIsNone(seen["org"])
