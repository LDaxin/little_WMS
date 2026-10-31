from django.contrib.auth.models import Permission, User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType
from loans.models import Lending, Loan, LoanOffer, LoanOfferItem, OrganisationMembership
from organisation.models import Organisation, Role, UserProfile


def user_with(organisation, username, *codenames):
    user = User.objects.create_user(username, password="pw")
    role = Role.objects.create(organisation=organisation, name="Role " + username)
    role.permissions.set(Permission.objects.filter(codename__in=codenames))
    UserProfile.objects.create(user=user, organisation=organisation, role=role)
    return user


class LendingTest(TestCase):
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

    def test_create_lending(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._lend(borrower_email="a@b.st", end_date="2026-08-10")
        lending = Lending.objects.get()
        self.assertEqual(lending.borrower_name, "Anna")
        self.assertEqual(lending.calendar_entry.entry_type, "loan")
        self.assertEqual(str(lending.calendar_entry.start_date), "2026-08-01")

    def test_lending_in_calendar(self):
        user_with(self.org, "u", "article_move_all", "calendar_view_all")
        self.client.login(username="u", password="pw")
        self._lend()
        self.assertContains(self.client.get("/calendar/"), "Loan: Jurte to Anna")

    def test_return_lending(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._lend()
        lending = Lending.objects.get()
        self.client.post("/lendings/%s/return/" % lending.pk)
        lending.refresh_from_db()
        self.assertEqual(lending.status, "returned")

    def test_permission(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        self.assertEqual(self._lend().status_code, 403)


class LoanTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.article_type = ArticleType.objects.create(name="tent", symbol="TZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Jurte", pType=cls.article_type, organisation=cls.org)
        cls.article = Article.objects.create(base=cls.base, organisation=cls.org)

    def _borrow(self, **extra):
        data = {"lender_type": "person", "lender_name": "Anna", "start_date": "2026-08-01"}
        data.update(extra)
        return self.client.post("/article/tent/%s/borrow" % self.article.pk, data)

    def test_borrow_from_person(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._borrow(end_date="2026-08-10")
        loan = Loan.objects.get()
        self.assertEqual(loan.lender_type, "person")
        self.assertEqual(loan.lender_name, "Anna")
        self.article.refresh_from_db()
        self.assertEqual(self.article.ownership, "borrowed")

    def test_borrow_from_organisation(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        lender = Organisation.objects.create(name="B", slug="b")
        self._borrow(lender_type="organisation", lender_organisation=lender.pk)
        loan = Loan.objects.get()
        self.assertEqual(loan.lender_organisation, lender)

    def test_return_loan(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")
        self._borrow()
        loan = Loan.objects.get()
        self.client.post("/loans/%s/return/" % loan.pk)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "returned")
        self.article.refresh_from_db()
        self.assertEqual(self.article.ownership, "owned")

    def test_permission(self):
        user_with(self.org, "u", "article_view_all")
        self.client.login(username="u", password="pw")
        self.assertEqual(self._borrow().status_code, 403)


class LoanOfferTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organisation.objects.create(name="A", slug="a")
        cls.lender = Organisation.objects.create(name="B", slug="b")
        cls.article_type = ArticleType.objects.create(name="tent", symbol="TZ", organisation=cls.org)
        cls.base = ArticleBase.objects.create(name="Jurte", pType=cls.article_type, organisation=cls.org)
        cls.article = Article.objects.create(base=cls.base, organisation=cls.org)

    def setUp(self):
        user_with(self.org, "u", "article_move_all")
        self.client.login(username="u", password="pw")

    def _offer(self, requires_confirmation):
        offer = LoanOffer.objects.create(
            lender_organisation=self.lender, name="Pool",
            requires_confirmation=requires_confirmation, organisation=self.org,
        )
        LoanOfferItem.objects.create(offer=offer, article=self.article, organisation=self.org)
        return offer

    def test_create_offer(self):
        self.client.post("/loan-offers/create/", {"name": "Pool", "requires_confirmation": "on"})
        offer = LoanOffer.objects.get()
        self.assertEqual(offer.name, "Pool")
        self.assertTrue(offer.requires_confirmation)

    def test_confirmation_resolution(self):
        offer = self._offer(True)
        item = offer.items.get()
        self.assertTrue(item.needs_confirmation())
        item.requires_confirmation = False
        item.save()
        self.assertFalse(item.needs_confirmation())

    def test_borrow_pending(self):
        offer = self._offer(True)
        item = offer.items.get()
        self.client.post("/loan-offers/%s/borrow/" % offer.pk, {"item_%s" % item.pk: "on", "start_date": "2026-08-01"})
        self.assertEqual(Loan.objects.get().status, "pending")

    def test_borrow_active(self):
        offer = self._offer(False)
        item = offer.items.get()
        self.client.post("/loan-offers/%s/borrow/" % offer.pk, {"item_%s" % item.pk: "on", "start_date": "2026-08-01"})
        self.assertEqual(Loan.objects.get().status, "active")

    def test_confirm(self):
        offer = self._offer(True)
        item = offer.items.get()
        self.client.post("/loan-offers/%s/borrow/" % offer.pk, {"item_%s" % item.pk: "on", "start_date": "2026-08-01"})
        loan = Loan.objects.get()
        self.client.post("/loans/%s/confirm/" % loan.pk)
        loan.refresh_from_db()
        self.assertEqual(loan.status, "active")

    def test_membership(self):
        membership = OrganisationMembership.objects.create(pool=self.lender, member=self.org)
        self.assertTrue(membership.can_borrow)
        self.assertFalse(membership.can_add)
