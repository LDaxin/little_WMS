from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from loans.models import Loan
from organisation.models import Organisation, Role, UserProfile


def user_with(organisation, username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation=organisation, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, organisation=organisation, role=role)
    return user


class LoanTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tent", symbol="TZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Jurte", pType=cls.article_type, organisation=cls.org)
        cls.article = Article.objects.create(base=cls.base, organisation=cls.org)

    def _lend(self, **extra):
        data = {"borrower_name": "Anna", "start_date": "2026-08-01"}
        data.update(extra)
        return self.client.post("/article/tent/%s/lend" % self.article.pk, data)

    def test_create_loan(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._lend(borrower_email="a@b.st", end_date="2026-08-10")
        loan = Loan.objects.get()
        self.assertEqual(loan.borrower_name, "Anna")
        self.assertEqual(loan.calendar_entry.entry_type, "loan")
        self.assertEqual(str(loan.calendar_entry.start_date), "2026-08-01")
        self.assertEqual(str(loan.calendar_entry.end_date), "2026-08-10")

    def test_loan_in_calendar(self):
        user_with(self.org, "u", "article_move_all", "calendar_view_all")
        self.client.login(username="u", password="pw")
        self._lend()
        self.assertContains(self.client.get("/calendar/"), "Loan: Jurte to Anna")

    def test_return(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._lend()
        loan = Loan.objects.get()
        self.client.post("/loans/%s/return/" % loan.pk)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "returned")

    def test_permission(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        self.assertEqual(self._lend().status_code, 403)
