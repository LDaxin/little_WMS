"""Saved views and share links (§10)."""
import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from organisation.decorators import require_scope
from organisation.permissions import has_perm
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


def _share_mode(request, link):
    """The permission source for a share view: the link or the user's role (§10)."""
    if not request.user.is_authenticated:
        return "link"
    return request.session.get("share_%s_mode" % link.pk, "link")


def shareLinkMode(request, token):
    """Switch a share view between the link's permissions and the user's role (§10)."""
    link = get_object_or_404(ShareLink, token=token)
    if request.method == "POST" and request.user.is_authenticated:
        mode = request.POST.get("mode", "link")
        if mode in ("link", "mine"):
            request.session["share_%s_mode" % link.pk] = mode
    return redirect("share link", token=token)


def shareLinkView(request, token):
    """Public capability URL: show a saved view read-only (§10)."""
    from article.models import Article
    from querybuilder.services import ARTICLE_FIELDS, QueryError, parse

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
        articles = articles.filter(parse(link.saved_view.query, ARTICLE_FIELDS))
    except QueryError:
        pass

    mode = _share_mode(request, link)
    can_borrow = request.user.is_authenticated and has_perm(
        request.user, "article.move_all", link=link if mode == "link" else None
    )

    if request.method == "POST" and can_borrow:
        from datetime import date

        from loans.models import Loan
        from planning.models import CalendarEntry

        for article in articles:
            if not request.POST.get("article_%s" % article.pk):
                continue
            status = "pending" if link.requires_confirmation else "active"
            entry = CalendarEntry.objects.create(
                entry_type="loan",
                title="Loan: %s from %s" % (article.base.name, link.saved_view.organisation),
                start_date=date.today().isoformat(),
                article=article,
                responsible_user=request.user,
            )
            Loan.objects.create(
                article=article,
                calendar_entry=entry,
                direction="in",
                party_type="organisation",
                party_organisation=link.saved_view.organisation,
                status=status,
            )
        return redirect("loans")

    if link.single_use:
        link.used_count += 1
        link.save()

    return render(request, "savedviews/shareView.html", {
        "link": link, "articles": articles, "can_borrow": can_borrow, "mode": mode,
    })
