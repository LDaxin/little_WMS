"""Saved views (§10)."""
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from organisation.decorators import require_scope
from savedviews.models import SavedView


def visible_views(user):
    """The user's own views and the organisation's shared ones."""
    return SavedView.objects.filter(Q(owner=user) | Q(is_shared=True))


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def savedViews(request):
    return render(request, "savedviews/savedViews.html", {
        "views": visible_views(request.user),
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
