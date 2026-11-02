from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from loans.models import LendLink, Loan, OrganisationMembership
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

    def _borrow(self, **extra):
        data = {"lender_type": "person", "lender_name": "Anna", "start_date": "2026-08-01"}
        data.update(extra)
        return self.client.post("/article/tent/%s/borrow" % self.article.pk, data)

    def test_lend_out(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._lend(borrower_email="a@b.st", end_date="2026-08-10")
        loan = Loan.objects.get()
        self.assertEqual(loan.direction, "out")
        self.assertEqual(loan.party_name, "Anna")
        self.assertEqual(loan.party_email, "a@b.st")
        self.assertEqual(loan.calendar_entry.entry_type, "loan")
        self.assertEqual(str(loan.calendar_entry.start_date), "2026-08-01")

    def test_lend_in_calendar(self):
        user_with(self.org, "u", "article_move_all", "calendar_view_all")
        self.client.login(username="u", password="pw")
        self._lend()
        self.assertContains(self.client.get("/calendar/"), "Loan: Jurte to Anna")

    def test_return_lent(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._lend()
        loan = Loan.objects.get()
        self.client.post("/loans/%s/return/" % loan.pk)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "returned")

    def test_borrow_from_person(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._borrow(end_date="2026-08-10")
        loan = Loan.objects.get()
        self.assertEqual(loan.direction, "in")
        self.assertEqual(loan.party_name, "Anna")
        self.article.refresh_from_db()
        self.assertEqual(self.article.ownership, "borrowed")

    def test_borrow_from_organisation(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        lender = Organisation.objects.create(name="B", slug="b")
        self._borrow(lender_type="organisation", lender_organisation=lender.pk)
        loan = Loan.objects.get()
        self.assertEqual(loan.party_organisation, lender)

    def test_return_borrowed(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._borrow()
        loan = Loan.objects.get()
        self.client.post("/loans/%s/return/" % loan.pk)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "returned")
        self.article.refresh_from_db()
        self.assertEqual(self.article.ownership, "owned")

    def test_list_shows_both_directions(self):
        user_with(self.org, "u", "article_move_all", "article_view_all")
        self.client.login(username="u", password="pw")
        self._lend()
        self._borrow()
        response = self.client.get("/loans/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lent out")
        self.assertContains(response, "Borrowed in")

    def test_permission(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        self.assertEqual(self._lend().status_code, 403)
        self.assertEqual(self._borrow().status_code, 403)


class MembershipTest(TestCase):
    def test_membership(self):
        pool = Organisation.objects.create(name="B", slug="b")
        member = Organisation.objects.create(name="A", slug="a")
        membership = OrganisationMembership.objects.create(pool=pool, member=member)
        self.assertTrue(membership.can_borrow)
        self.assertFalse(membership.can_add)


class LendLinkTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.first()

    def _link(self, **kwargs):
        return LendLink.objects.create(organisation=self.org, lender_name="Anna", **kwargs)

    def test_create_and_revoke(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self.client.post("/lend-links/", {"label": "Camp"})
        link = LendLink.objects.get()
        self.assertEqual(link.label, "Camp")
        self.client.post("/lend-links/%s/revoke/" % link.pk)
        link.refresh_from_db()
        self.assertFalse(link.is_active)

    def test_lender_details(self):
        link = LendLink.objects.create(organisation=self.org)
        self.client.post("/lend/%s/" % link.token, {"lender_name": "Anna", "lender_email": "a@b.st"})
        link.refresh_from_db()
        self.assertEqual(link.lender_name, "Anna")
        self.assertEqual(link.lender_email, "a@b.st")

    def test_add_item(self):
        link = self._link()
        self.client.post("/lend/%s/" % link.token, {
            "action": "add", "name": "Zelt", "description": "blue",
            "start_date": "2026-08-01", "end_date": "2026-08-10",
        })
        loan = Loan.objects.get()
        self.assertEqual(loan.direction, "in")
        self.assertEqual(loan.party_name, "Anna")
        self.assertEqual(loan.article.base.name, "Zelt")
        self.assertEqual(loan.lend_link, link)

    def test_edit_item(self):
        link = self._link()
        self.client.post("/lend/%s/" % link.token, {"action": "add", "name": "Zelt", "start_date": "2026-08-01"})
        loan = Loan.objects.get()
        self.client.post("/lend/%s/" % link.token, {
            "action": "edit", "loan": loan.pk, "name": "Zelt 2", "start_date": "2026-09-01",
        })
        loan.refresh_from_db()
        self.assertEqual(loan.article.base.name, "Zelt 2")
        self.assertEqual(str(loan.calendar_entry.start_date), "2026-09-01")

    def test_delete_item(self):
        link = self._link()
        self.client.post("/lend/%s/" % link.token, {"action": "add", "name": "Zelt", "start_date": "2026-08-01"})
        loan = Loan.objects.get()
        self.client.post("/lend/%s/" % link.token, {"action": "delete", "loan": loan.pk})
        self.assertFalse(Loan.objects.filter(pk=loan.pk, deleted_at__isnull=True).exists())

    def test_revoke_removes_and_anonymises(self):
        link = self._link()
        self.client.post("/lend/%s/" % link.token, {"action": "add", "name": "Zelt", "start_date": "2026-08-01"})
        loan = Loan.objects.get()
        article_id = loan.article_id
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self.client.post("/lend-links/%s/revoke/" % link.pk)
        self.assertFalse(Loan.objects.filter(pk=loan.pk, deleted_at__isnull=True).exists())
        self.assertFalse(Article.objects.filter(pk=article_id, deleted_at__isnull=True).exists())
        link.refresh_from_db()
        self.assertEqual(link.lender_name, "")

    def test_invalid_link(self):
        link = LendLink.objects.create(organisation=self.org, is_active=False)
        response = self.client.get("/lend/%s/" % link.token)
        self.assertContains(response, "no longer valid")
