"""Loans (§20)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from article.models import Article, ArticleBase, ArticleImage, ArticleType, Stock
from audit.services import log as audit_log
from loans.models import LendLink, Loan
from occasion.models import Occasion
from organisation.decorators import require_scope
from organisation.models import Organisation
from organisation.services import active_organisation
from planning.models import CalendarEntry


def _occasion(request):
    return Occasion.objects.filter(pk=request.POST.get("occasion") or None).first()


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def loans(request):
    return render(request, "loans/loans.html", {
        "loans": Loan.objects.select_related("article__base", "calendar_entry"),
    })


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def lendArticle(request, typ, articleId):
    """Lend an article to an external person (direction "out", §20)."""
    article = Article.objects.get(pk=articleId)
    if request.method == "POST":
        name = request.POST.get("borrower_name", "").strip()
        start = request.POST.get("start_date", "")
        if name and start:
            entry = CalendarEntry.objects.create(
                entry_type="loan",
                title="Loan: %s to %s" % (article.base.name, name),
                start_date=start,
                end_date=request.POST.get("end_date") or None,
                article=article,
                responsible_user=request.user,
            )
            Loan.objects.create(
                article=article,
                calendar_entry=entry,
                direction="out",
                party_name=name,
                party_email=request.POST.get("borrower_email", "").strip(),
                occasion=_occasion(request),
            )
    if request.headers.get("HX-Request"):
        from article.views import _calendar_context
        return render(request, "hub/modules/articleCalendar.html",
                      _calendar_context(article, request, typ))
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def borrowArticle(request, typ, articleId):
    """Borrow an article from an external lender (direction "in", §20)."""
    article = Article.objects.get(pk=articleId)
    if request.method == "POST":
        start = request.POST.get("start_date", "")
        if start:
            name = request.POST.get("lender_name", "").strip()
            party_org = Organisation.objects.filter(
                pk=request.POST.get("lender_organisation") or None
            ).first()
            party = name or (party_org.name if party_org else "")
            entry = CalendarEntry.objects.create(
                entry_type="loan",
                title="Loan: %s from %s" % (article.base.name, party),
                start_date=start,
                end_date=request.POST.get("end_date") or None,
                article=article,
                responsible_user=request.user,
            )
            Loan.objects.create(
                article=article,
                calendar_entry=entry,
                direction="in",
                party_type=request.POST.get("lender_type", "person"),
                party_name=name,
                party_organisation=party_org,
                occasion=_occasion(request),
            )
    if request.headers.get("HX-Request"):
        from article.views import _calendar_context
        return render(request, "hub/modules/articleCalendar.html",
                      _calendar_context(article, request, typ))
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def returnLoan(request, loanId):
    loan = get_object_or_404(Loan, pk=loanId)
    if request.method == "POST":
        loan.status = "returned"
        loan.save()
    return redirect("loans")


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def confirmLoan(request, loanId):
    loan = get_object_or_404(Loan, pk=loanId)
    if request.method == "POST":
        loan.status = "active"
        loan.save()
    return redirect("loans")


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def lendLinks(request):
    """List and create lend links (§20)."""
    organisation = active_organisation(request)
    if request.method == "POST":
        LendLink.objects.create(
            organisation=organisation,
            label=request.POST.get("label", "").strip(),
            created_by=request.user,
        )
        return redirect("lend links")
    return render(request, "loans/lendLinks.html", {
        "links": LendLink.objects.filter(organisation=organisation),
    })


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def lendLinkRevoke(request, linkId):
    """Deactivate a lend link: remove its items and anonymise the lender (§20)."""
    link = get_object_or_404(LendLink, pk=linkId, organisation=active_organisation(request))
    if request.method == "POST":
        link.is_active = False
        link.lender_name = ""
        link.lender_email = ""
        link.save()
        for loan in link.loans.all():
            _delete_lend(loan)
    return redirect("lend links")


def _create_lend(link, request):
    """Create the borrowed article, loan and calendar entry for a lend link (§20)."""
    organisation = link.organisation
    article_type, _ = ArticleType.objects.get_or_create(
        organisation=organisation, name="borrowed", defaults={"symbol": "LE"}
    )
    base = ArticleBase.objects.create(
        organisation=organisation, name=request.POST["name"].strip(), pType=article_type
    )
    article = Article.objects.create(
        organisation=organisation, base=base,
        notiz=request.POST.get("description", "").strip(),
    )
    Stock.objects.create(article=article, stored=None, menge=1)
    photo = request.FILES.get("photo")
    if photo:
        ArticleImage.objects.create(article=article, image=photo)

    entry = CalendarEntry.objects.create(
        organisation=organisation,
        entry_type="loan",
        title="Loan: %s from %s" % (base.name, link.lender_name),
        start_date=request.POST["start_date"],
        end_date=request.POST.get("end_date") or None,
        article=article,
    )
    audit_log("created", article, None, {"name": base.name})
    return Loan.objects.create(
        organisation=organisation,
        article=article,
        calendar_entry=entry,
        direction="in",
        party_type="person",
        party_name=link.lender_name,
        party_email=link.lender_email,
        lend_link=link,
    )


def _delete_lend(loan):
    """Remove a lent item for good and anonymise its audit trail (§20).

    Mirrors the GDPR user deletion: the audit entries are anonymised and the
    article (with its loan, calendar entry, stock and images) is hard-deleted,
    so nothing is left in the trash.
    """
    from django.contrib.contenttypes.models import ContentType

    from audit.models import AuditLog

    article = loan.article
    AuditLog.objects.filter(
        content_type=ContentType.objects.get_for_model(article), object_id=article.pk
    ).update(user=None, changes={})
    article.hard_delete()


def _edit_lend(loan, request):
    """Update a lent item's name, description and period (§20)."""
    name = request.POST.get("name", "").strip()
    if name and len(name) <= 20:
        loan.article.base.name = name
        loan.article.base.save()
    loan.article.notiz = request.POST.get("description", "").strip()
    loan.article.save()
    entry = loan.calendar_entry
    if request.POST.get("start_date"):
        entry.start_date = request.POST["start_date"]
    entry.end_date = request.POST.get("end_date") or None
    entry.save()


def lendLinkView(request, token):
    """Public capability URL: an external person manages their lent items (§20)."""
    link = get_object_or_404(LendLink, token=token)
    if not link.is_valid():
        return render(request, "loans/lendLink.html", {"link": link, "invalid": True})

    error = ""
    if request.method == "POST":
        action = request.POST.get("action")
        if not link.lender_name:
            name = request.POST.get("lender_name", "").strip()
            if name:
                link.lender_name = name
                link.lender_email = request.POST.get("lender_email", "").strip()
                link.save()
                return redirect("lend link", token=token)
            error = "Please enter your name."
        elif action == "add":
            name = request.POST.get("name", "").strip()
            start = request.POST.get("start_date", "")
            if not name or not start:
                error = "Please fill in the item name and the start date."
            elif len(name) > 20:
                error = "The item name is too long (max 20 characters)."
            else:
                _create_lend(link, request)
                return redirect("lend link", token=token)
        elif action == "edit":
            loan = link.loans.filter(pk=request.POST.get("loan")).first()
            if loan:
                _edit_lend(loan, request)
                return redirect("lend link", token=token)
        elif action == "delete":
            loan = link.loans.filter(pk=request.POST.get("loan")).first()
            if loan:
                _delete_lend(loan)
                return redirect("lend link", token=token)
        elif action == "delete_all":
            for loan in link.loans.all():
                _delete_lend(loan)
            return redirect("lend link", token=token)

    return render(request, "loans/lendLink.html", {
        "link": link,
        "loans": link.loans.select_related("article__base", "calendar_entry"),
        "error": error,
    })
