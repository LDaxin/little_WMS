"""Saved views and share links (§10)."""
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from organisation.decorators import require_scope
from savedviews.models import SavedView, ShareLink


def visible_views(user):
    """The user's own views and the organisation's shared ones."""
    return SavedView.objects.filter(Q(owner=user) | Q(is_shared=True))


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def savedViews(request):
    return render(request, "savedviews/savedViews.html", {
        "views": visible_views(request.user),
        "links": ShareLink.objects.filter(saved_view__in=visible_views(request.user), is_active=True),
    })


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def saveSavedView(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        query = request.POST.get("query", "")
        if name and query:
            try:
                parsed = json.loads(query)
            except ValueError:
                parsed = {}
            SavedView.objects.create(
                owner=request.user,
                name=name,
                typ=request.POST.get("typ", ""),
                query=parsed,
                is_shared=request.POST.get("is_shared") == "on",
            )
    return redirect(request.POST.get("next") or "saved views")


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def delSavedView(request, viewId):
    saved_view = get_object_or_404(SavedView, pk=viewId, owner=request.user)
    if request.method == "POST":
        saved_view.delete()
    return redirect("saved views")


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def toggleDashboard(request, viewId):
    saved_view = get_object_or_404(SavedView, pk=viewId, owner=request.user)
    if request.method == "POST":
        saved_view.show_on_dashboard = not saved_view.show_on_dashboard
        saved_view.save()
    return redirect("saved views")


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def shareSavedView(request, viewId):
    saved_view = get_object_or_404(SavedView, pk=viewId)
    if request.method == "POST":
        days = request.POST.get("days", "").strip()
        password = request.POST.get("password", "")
        ShareLink.objects.create(
            saved_view=saved_view,
            access_mode=request.POST.get("access_mode", "public"),
            permissions=["view", "borrow"] if request.POST.get("allow_borrow") == "on" else ["view"],
            requires_confirmation=request.POST.get("requires_confirmation") == "on",
            expires_at=timezone.now() + timedelta(days=int(days)) if days.isdigit() else None,
            single_use=request.POST.get("single_use") == "on",
            password_hash=make_password(password) if password else "",
            created_by=request.user,
        )
    return redirect("saved views")


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def revokeShareLink(request, linkId):
    link = get_object_or_404(ShareLink, pk=linkId)
    if request.method == "POST":
        link.is_active = False
        link.save()
    return redirect("saved views")


def shareLinkView(request, token):
    """Public capability URL: show a saved view read-only (§10)."""
    from article.models import Article
    from querybuilder.services import ARTICLE_FIELDS, QueryError, parse_json

    link = get_object_or_404(ShareLink, token=token)
    if not link.is_valid():
        return render(request, "savedviews/shareInvalid.html", {"link": link})

    session_key = "share_%s" % link.pk
    if link.password_hash and not request.session.get(session_key):
        error = ""
        if request.method == "POST":
            if check_password(request.POST.get("password", ""), link.password_hash):
                request.session[session_key] = True
                return redirect("share link", token=token)
            error = "Wrong password"
        return render(request, "savedviews/sharePassword.html", {"link": link, "error": error})

    articles = Article.objects.all()
    try:
        articles = articles.filter(parse_json(json.dumps(link.saved_view.query), ARTICLE_FIELDS))
    except QueryError:
        pass

    if request.method == "POST" and link.can_borrow() and request.user.is_authenticated:
        from datetime import date

        from loans.models import Loan
        from organisation.services import active_organisation

        for article in articles:
            if not request.POST.get("article_%s" % article.pk):
                continue
            status = "pending" if link.requires_confirmation else "active"
            Loan.objects.create(
                article=article,
                lender_type="organisation",
                lender_organisation=link.saved_view.organisation,
                borrower_organisation=active_organisation(request),
                start_date=date.today().isoformat(),
                status=status,
            )
            if status == "active":
                article.ownership = "borrowed"
                article.save()
        return redirect("loans")

    if link.single_use:
        link.used_count += 1
        link.save()

    return render(request, "savedviews/shareView.html", {"link": link, "articles": articles})
