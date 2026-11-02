"""Loans (§20)."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from article.models import Article
from loans.models import Loan
from occasion.models import Occasion
from organisation.decorators import require_scope
from organisation.models import Organisation
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
