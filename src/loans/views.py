"""Loans (§20)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from article.models import Article, ArticleBase, ArticleImage, ArticleType, Stock
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
            article.ownership = "borrowed"
            article.save()
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def returnLoan(request, loanId):
    loan = get_object_or_404(Loan, pk=loanId)
    if request.method == "POST":
        loan.status = "returned"
        loan.save()
        if loan.direction == "in":
            loan.article.ownership = "owned"
            loan.article.save()
    return redirect("loans")


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def confirmLoan(request, loanId):
    loan = get_object_or_404(Loan, pk=loanId)
    if request.method == "POST":
        loan.status = "active"
        loan.save()
        if loan.direction == "in":
            loan.article.ownership = "borrowed"
            loan.article.save()
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
            single_use=request.POST.get("single_use") == "on",
            created_by=request.user,
        )
        return redirect("lend links")
    return render(request, "loans/lendLinks.html", {
        "links": LendLink.objects.filter(organisation=organisation),
    })


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def lendLinkRevoke(request, linkId):
    link = get_object_or_404(LendLink, pk=linkId, organisation=active_organisation(request))
    if request.method == "POST":
        link.is_active = False
        link.save()
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
        notiz=request.POST.get("description", "").strip(), ownership="borrowed",
    )
    Stock.objects.create(article=article, stored=None, menge=1)
    photo = request.FILES.get("photo")
    if photo:
        ArticleImage.objects.create(article=article, image=photo)

    entry = CalendarEntry.objects.create(
        organisation=organisation,
        entry_type="loan",
        title="Loan: %s from %s" % (base.name, request.POST["friend_name"].strip()),
        start_date=request.POST["start_date"],
        end_date=request.POST.get("end_date") or None,
        article=article,
    )
    return Loan.objects.create(
        organisation=organisation,
        article=article,
        calendar_entry=entry,
        direction="in",
        party_type="person",
        party_name=request.POST["friend_name"].strip(),
        party_email=request.POST.get("friend_email", "").strip(),
    )


def lendLinkView(request, token):
    """Public capability URL: an external person lends an item (§20)."""
    link = get_object_or_404(LendLink, token=token)
    if not link.is_valid():
        return render(request, "loans/lendLink.html", {"link": link, "invalid": True})

    session_key = "lend_%s" % link.pk
    loan_id = request.session.get(session_key)
    if loan_id:
        return render(request, "loans/lendLink.html", {
            "link": link, "loan": Loan.objects.filter(pk=loan_id).first(),
        })

    error = ""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        friend = request.POST.get("friend_name", "").strip()
        start = request.POST.get("start_date", "")
        if not name or not friend or not start:
            error = "Please fill in the item name, your name, and the start date."
        elif len(name) > 20:
            error = "The item name is too long (max 20 characters)."
        else:
            loan = _create_lend(link, request)
            request.session[session_key] = loan.pk
            if link.single_use:
                link.used_count += 1
                link.save()
            return redirect("lend link", token=token)
    return render(request, "loans/lendLink.html", {"link": link, "error": error})
