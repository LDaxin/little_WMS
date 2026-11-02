"""Inventory mode (§5c).

Scan a location to set the scope, then scan the articles found there. The
expected list is the current ``Stock`` in that location; scanned articles that
belong elsewhere are flagged as deviations. State lives in the user's session,
like the movement buffer.
"""

from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound
from django.shortcuts import render

from article.models import Article, Stock
from storage.models import Storage
from space.services import space_path
from codeSystem.services import resolve_code
from hub.csv import csv_response
from hub.search import filter_by_search


def _get_state(session):
    state = session.get("inventory")
    if not state:
        state = {"space": None, "scanned": []}
        session["inventory"] = state
    return state


def _save_state(session, state):
    session["inventory"] = state
    session.modified = True


def _resolve_location(code):
    """The Storage/Article behind a location code, for display."""
    if not code:
        return None
    return resolve_code(code)[1]


def _context(request, error="", success=""):
    state = _get_state(request.session)
    location = _resolve_location(state["space"])
    scanned = set(state["scanned"])

    expected = []
    if location is not None:
        stocks = Stock.objects.filter(stored=location.space).select_related("article__base")
        for stock in stocks:
            code = stock.article.code.code
            expected.append({"article": stock.article, "found": code in scanned})
    expected_codes = {e["article"].code.code for e in expected}

    deviations = []
    for code in state["scanned"]:
        if code in expected_codes:
            continue
        article = Article.objects.filter(code__code=code).first()
        if article is None:
            continue
        deviations.append({
            "article": article,
            "locations": [space_path(s.stored) for s in article.stocks.exclude(stored=None)],
        })

    return {
        "location": location,
        "expected": expected,
        "deviations": deviations,
        "scanned_count": len(state["scanned"]),
        "expected_count": len(expected),
        "found_count": sum(1 for e in expected if e["found"]),
        "error": error,
        "success": success,
    }


def _render(request, error="", success=""):
    return render(request, "movement/inventoryBody.html",
                  context=_context(request, error=error, success=success))


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def inventory(request):
    return render(request, "movement/inventory.html", context=_context(request))


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def inventoryScan(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = _get_state(request.session)
    code = request.POST.get("code", "").strip()
    error = ""
    try:
        kind, obj = resolve_code(code)
        if kind is None:
            raise ValidationError("Unknown code %s" % code)
        if obj is None:
            error = "No object with code %s" % code
        elif kind == "storage":
            state["space"] = code
        else:  # article
            if not state["space"]:
                raise ValidationError("Scan a location first")
            if code not in state["scanned"]:
                state["scanned"].append(code)
    except ValidationError as e:
        error = e.messages[0] if e.messages else str(e)

    _save_state(request.session, state)
    return _render(request, error=error)


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def inventoryClear(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    _save_state(request.session, {"space": None, "scanned": []})
    return _render(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def inventorySearch(request):
    """Live suggestions for the combined code/name field (§5c)."""
    search = request.GET.get("code", "").strip()
    if search == "":
        articles = Article.objects.none()
        storages = Storage.objects.none()
    else:
        articles = filter_by_search(Article.objects.all(), search, "base__name", "code__code")[:20]
        storages = filter_by_search(Storage.objects.all(), search, "name", "code__code")[:20]
    return render(request, "movement/inventoryResults.html",
                  context={"resultsA": articles, "resultsS": storages})


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def inventoryExport(request):
    context = _context(request)
    location = str(context["location"]) if context["location"] else ""
    rows = [
        [e["article"].base.name, e["article"].code.code, "found" if e["found"] else "not found", location]
        for e in context["expected"]
    ]
    rows += [
        [d["article"].base.name, d["article"].code.code, "deviation", "; ".join(d["locations"])]
        for d in context["deviations"]
    ]
    return csv_response("inventory.csv", ["name", "code", "status", "location"], rows)
