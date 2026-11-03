from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from organisation.models import Role, UserProfile


def user_with(username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation_id=1, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, role=role, organisation_id=1)
    return user


class AssignedScopeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        article_type = ArticleType.objects.create(name="werkzeug", symbol="WZ")
        base = ArticleBase.objects.create(name="Hammer", pType=article_type)
        cls.article = Article.objects.create(base=base)
        Stock.objects.create(article=cls.article, stored=None, menge=1)

    def detail_url(self):
        return "/article/werkzeug/%s/" % self.article.pk

    def test_assigned_only_list_is_filtered(self):
        user_with("viewer", "article_view_assigned")
        self.client.login(username="viewer", password="pw")
        response = self.client.get("/article/werkzeug/search", {"search": ""})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.article.code.code)

    def test_view_all_list_shows_unassigned(self):
        user_with("boss", "article_view_all")
        self.client.login(username="boss", password="pw")
        response = self.client.get("/article/werkzeug/search", {"search": ""})
        self.assertContains(response, self.article.code.code)

    def test_assigned_only_detail_of_unassigned_is_forbidden(self):
        user_with("viewer", "article_view_assigned")
        self.client.login(username="viewer", password="pw")
        self.assertEqual(self.client.get(self.detail_url()).status_code, 403)

    def test_assigned_only_detail_of_assigned_works(self):
        user = user_with("viewer", "article_view_assigned")
        self.article.assigned_to.add(user)
        self.client.login(username="viewer", password="pw")
        self.assertEqual(self.client.get(self.detail_url()).status_code, 200)

    def test_assigned_only_edit_of_unassigned_is_forbidden(self):
        user_with("editor", "article_edit_assigned")
        self.client.login(username="editor", password="pw")
        self.assertEqual(
            self.client.post("/article/werkzeug/%s/update" % self.article.pk, {}).status_code,
            403,
        )

    def test_assign_and_unassign(self):
        user = user_with("boss", "article_edit_all")
        assignee = User.objects.create_user("helper", password="pw")
        self.client.login(username="boss", password="pw")
        self.client.post("/article/werkzeug/%s/assign" % self.article.pk, {"user": assignee.pk})
        self.assertIn(assignee, self.article.assigned_to.all())
        self.client.post("/article/werkzeug/%s/unassign/%s" % (self.article.pk, assignee.pk))
        self.assertNotIn(assignee, self.article.assigned_to.all())
