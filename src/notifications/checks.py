"""Notification triggers (§6).

This layer only knows *what* is due; it yields ``Finding``s. Turning findings
into notifications (or anything else) is a separate consumer, so other consumers
(email, webhook, dashboard) can reuse the same findings later.
"""
from dataclasses import dataclass
from datetime import date, timedelta

from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext as _


@dataclass
class Finding:
    trigger_type: str
    title: str
    message: str = ""
    link: str = ""
    dedupe_key: str = ""


def expiry_findings(organisation, days=7):
    """Articles expiring within ``days``."""
    from article.models import Article

    limit = date.today() + timedelta(days=days)
    articles = Article.objects.filter(
        organisation=organisation, ablaufdatum__isnull=False, ablaufdatum__lte=limit
    )
    for article in articles:
        yield Finding(
            trigger_type="expiry_date_reached",
            title=_("Article expires soon: %(name)s") % {"name": article.base.name},
            message=_("Expires on %(date)s") % {"date": article.ablaufdatum},
            link=reverse("article", args=[article.base.pType.name, article.pk]),
            dedupe_key="expiry:%s" % article.pk,
        )


def maintenance_findings(organisation):
    """Maintenance entries that are due."""
    from planning.models import CalendarEntry

    entries = CalendarEntry.objects.filter(
        organisation=organisation, entry_type="maintenance", start_date__lte=date.today()
    )
    for entry in entries:
        link = ""
        if entry.article_id:
            link = reverse("article", args=[entry.article.base.pType.name, entry.article_id])
        yield Finding(
            trigger_type="maintenance_due",
            title=_("Maintenance due: %(title)s") % {"title": entry.title},
            link=link,
            dedupe_key="maintenance:%s" % entry.pk,
        )


def low_stock_findings(organisation):
    """Articles whose total stock is below the base's minimum."""
    from article.models import ArticleBase, Stock

    bases = ArticleBase.objects.filter(organisation=organisation, mindestbestand__isnull=False)
    for base in bases:
        total = Stock.objects.filter(article__base=base).aggregate(total=Sum("menge"))["total"] or 0
        if total < base.mindestbestand:
            yield Finding(
                trigger_type="minimum_stock_undercut",
                title=_("Low stock: %(name)s") % {"name": base.name},
                message=_("%(total)s of %(min)s left") % {"total": total, "min": base.mindestbestand},
                dedupe_key="low_stock:%s" % base.pk,
            )


def return_overdue_findings(organisation):
    """Active loans whose return date has passed (§20)."""
    from loans.models import Lending, Loan

    today = date.today()
    lendings = Lending.objects.filter(
        organisation=organisation, status="active", calendar_entry__end_date__lt=today
    ).select_related("article__base", "calendar_entry")
    for lending in lendings:
        yield Finding(
            trigger_type="return_overdue",
            title=_("Loan overdue: %(name)s") % {"name": lending.article.base.name},
            message=_("Due %(date)s, borrowed by %(who)s") % {
                "date": lending.calendar_entry.end_date, "who": lending.borrower_name},
            link=reverse("article", args=[lending.article.base.pType.name, lending.article.pk]),
            dedupe_key="return_overdue:lending:%s" % lending.pk,
        )

    loans = Loan.objects.filter(
        organisation=organisation, status="active", end_date__lt=today
    ).select_related("article__base")
    for loan in loans:
        yield Finding(
            trigger_type="return_overdue",
            title=_("Return overdue: %(name)s") % {"name": loan.article.base.name},
            message=_("Due %(date)s") % {"date": loan.end_date},
            link=reverse("article", args=[loan.article.base.pType.name, loan.article.pk]),
            dedupe_key="return_overdue:loan:%s" % loan.pk,
        )


CHECKS = [expiry_findings, maintenance_findings, low_stock_findings, return_overdue_findings]


def run_checks(organisation, **kwargs):
    """Yield every finding for ``organisation``."""
    for check in CHECKS:
        yield from check(organisation, **kwargs)
