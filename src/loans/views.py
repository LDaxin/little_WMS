"""Loans (§20)."""
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from article.models import Article
from loans.models import Lending, Loan, LoanOffer, LoanOfferItem
from occasion.models import Occasion
from organisation.decorators import require_scope
from organisation.models import Organisation
from organisation.services import active_organisation
from planning.models import CalendarEntry


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def lendings(request):
    return render(request, "loans/lendings.html", {
        "lendings": Lending.objects.select_related("article__base", "calendar_entry"),
    })


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def lendArticle(request, typ, articleId):
    """Lend an article to an external person (§20)."""
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
            Lending.objects.create(
                article=article,
                calendar_entry=entry,
                borrower_name=name,
                borrower_email=request.POST.get("borrower_email", "").strip(),
                occasion=Occasion.objects.filter(pk=request.POST.get("occasion") or None).first(),
            )
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def returnLending(request, lendingId):
    lending = get_object_or_404(Lending, pk=lendingId)
    if request.method == "POST":
        lending.status = "returned"
        lending.save()
    return redirect("lendings")


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def loans(request):
    return render(request, "loans/loans.html", {
        "loans": Loan.objects.select_related("article__base"),
    })


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def borrowArticle(request, typ, articleId):
    """Record that the organisation borrows an article from an external lender (§20)."""
    article = Article.objects.get(pk=articleId)
    if request.method == "POST":
        start = request.POST.get("start_date", "")
        if start:
            Loan.objects.create(
                article=article,
                lender_type=request.POST.get("lender_type", "person"),
                lender_name=request.POST.get("lender_name", "").strip(),
                lender_organisation=Organisation.objects.filter(
                    pk=request.POST.get("lender_organisation") or None
                ).first(),
                occasion=Occasion.objects.filter(pk=request.POST.get("occasion") or None).first(),
                start_date=start,
                end_date=request.POST.get("end_date") or None,
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
        loan.article.ownership = "owned"
        loan.article.save()
    return redirect("loans")


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def loanOffers(request):
    return render(request, "loans/offers.html", {"offers": LoanOffer.objects.all()})


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def createLoanOffer(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            offer = LoanOffer.objects.create(
                lender_organisation=active_organisation(request),
                name=name,
                requires_confirmation=request.POST.get("requires_confirmation") == "on",
            )
            for article_id in request.POST.getlist("article"):
                article = Article.objects.filter(pk=article_id).first()
                if article:
                    LoanOfferItem.objects.create(offer=offer, article=article)
    return redirect("loan offers")


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def borrowFromOffer(request, offerId):
    offer = get_object_or_404(LoanOffer, pk=offerId)
    if request.method == "POST":
        start = request.POST.get("start_date") or date.today().isoformat()
        for item in offer.items.all():
            if not request.POST.get("item_%s" % item.pk):
                continue
            status = "pending" if item.needs_confirmation() else "active"
            Loan.objects.create(
                article=item.article,
                lender_type="organisation",
                lender_organisation=offer.lender_organisation,
                borrower_organisation=active_organisation(request),
                start_date=start,
                status=status,
            )
            if status == "active":
                item.article.ownership = "borrowed"
                item.article.save()
    return redirect("loans")


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def confirmLoan(request, loanId):
    loan = get_object_or_404(Loan, pk=loanId)
    if request.method == "POST":
        loan.status = "active"
        loan.save()
        loan.article.ownership = "borrowed"
        loan.article.save()
    return redirect("loans")
