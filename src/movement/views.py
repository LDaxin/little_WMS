from django.utils.translation import gettext as _
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from django.core.exceptions import ValidationError
from django.db.models import Q

from article.models import Article
from storage.models import Storage
from space.services import space_path
from codeSystem.services import resolve_code
from hub.search import filter_by_search
from movement.services import MovementService, resolve_space, undo
from movement.session import get_state, save_state, reset, get_open_session, end_open_session
from article.services import default_locations
from audit.models import AuditLog

# Create your views here.


def _resolve_target(code):
    """The Storage/Article behind a target code, for display."""
    if not code:
        return None
    return resolve_code(code)[1]


def _articles_from_codes(codes):
    by_code = {a.code.code: a for a in Article.objects.filter(code__code__in=codes)}
    articles = []
    for code in codes:
        if code not in by_code:
            raise ValidationError("No article with code %s" % code)
        articles.append(by_code[code])
    return articles


def _buffer_context(request, error="", success=""):
    state = get_state(request.session)
    by_code = {a.code.code: a for a in Article.objects.filter(code__code__in=state["buffer"])}
    buffered = [by_code[c] for c in state["buffer"] if c in by_code]
    session = get_open_session(request.user, create=False)
    entries = (
        AuditLog.objects.filter(session=session)[:20] if session is not None else []
    )
    return {
        "mode": state["mode"],
        "buffer": buffered,
        "target": _resolve_target(state["target"]),
        "target_smart": state["target_smart"],
        "session_entries": entries,
        "error": error,
        "success": success,
    }


def _render_buffer(request, error="", success="", trigger=""):
    response = render(request, "movement/buffer.html",
                      context=_buffer_context(request, error=error, success=success))
    if trigger:
        response["HX-Trigger"] = trigger
    return response


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movement(request):
    return render(request, "movement/movement.html", context=_buffer_context(request))


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def where(request):
    """'Where is...?' – current and default location of an article (§5b)."""
    query = request.GET.get("q", "").strip()
    article = None
    results = []
    if query:
        kind, article = resolve_code(query)
        if kind != "article":
            article = None
            results = Article.objects.filter(
                Q(base__name__contains=query) | Q(code__code__contains=query)
            )[:20]

    context = {
        "query": query,
        "article": article,
        "results": results,
        "current_paths": [space_path(s.stored) for s in article.stocks.exclude(stored=None)] if article else [],
        "default_paths": [space_path(loc) for loc in default_locations(article.base)] if article else [],
    }
    return render(request, "movement/where.html", context=context)


@login_required(login_url='/accounts/login/')
@require_perm("article.view_all")
def whereSearch(request):
    search = request.GET.get("q", "").strip()
    results = []
    if search:
        results = filter_by_search(Article.objects.all(), search, "base__name", "code__code")[:20]
    return render(request, "movement/whereResults.html", context={"results": results})


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementScan(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    code = request.POST.get("code", "").strip()
    error = ""
    try:
        kind, obj = resolve_code(code)
        if kind is None:
            raise ValidationError("Unknown code %s" % code)
        if obj is None:
            error = "No object with code %s" % code
        elif kind == "storage":
            state["target"] = code
            state["target_smart"] = False
        else:  # article
            if obj.space and obj.space.active and not state["target"]:
                # smart default: a container becomes the target
                state["target"] = code
                state["target_smart"] = True
            elif code not in state["buffer"]:
                state["buffer"].append(code)
    except ValidationError as e:
        error = e.messages[0] if e.messages else str(e)

    save_state(request.session, state)
    return _render_buffer(request, error=error,
                          trigger="movementError" if error else "movementScan")


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementMode(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    mode = request.POST.get("mode", "store")
    if mode in ("store", "remove"):
        state["mode"] = mode
    reset(request.session)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementClear(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    reset(request.session)
    end_open_session(request.user)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementBufferRemove(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    code = request.POST.get("code", "")
    if code in state["buffer"]:
        state["buffer"].remove(code)
    save_state(request.session, state)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementTargetClear(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    state["target"] = None
    state["target_smart"] = False
    save_state(request.session, state)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementTreatAsArticle(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    if state["target"] and state["target"] not in state["buffer"]:
        state["buffer"].append(state["target"])
    state["target"] = None
    state["target_smart"] = False
    save_state(request.session, state)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementSetTarget(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    code = request.POST.get("code", "")
    if code in state["buffer"]:
        state["buffer"].remove(code)
        state["target"] = code
        state["target_smart"] = False
    save_state(request.session, state)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementStore(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    try:
        target = resolve_space(state["target"] or "")
        articles = _articles_from_codes(state["buffer"])
        MovementService.store_articles(
            articles, target, request.user, session=get_open_session(request.user))
    except ValidationError as e:
        return _render_buffer(request, error=e.messages[0] if e.messages else str(e))

    count = len(articles)
    reset(request.session)
    return _render_buffer(request, success="Stored %s article(s)" % count)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementRemove(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    try:
        articles = _articles_from_codes(state["buffer"])
        session = get_open_session(request.user)
        for article in articles:
            MovementService.remove_article(article, user=request.user, session=session)
    except ValidationError as e:
        return _render_buffer(request, error=e.messages[0] if e.messages else str(e))

    count = len(articles)
    reset(request.session)
    return _render_buffer(request, success="Removed %s article(s)" % count)


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementUndo(request):
    """Undo the most recent (not yet undone) action of the open session (§11)."""
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    session = get_open_session(request.user)
    entry = (
        AuditLog.objects.filter(session=session, undone=False).first()
        if session is not None else None
    )
    if entry is None:
        return _render_buffer(request, error="Nothing to undo")
    try:
        undo(entry, request.user)
    except ValidationError as e:
        return _render_buffer(request, error=e.messages[0] if e.messages else str(e))
    return _render_buffer(request, success="Undone")


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementUndoEntry(request):
    """Undo one specific session entry (§11)."""
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    session = get_open_session(request.user)
    entry = AuditLog.objects.filter(
        pk=request.POST.get("entry"), session=session
    ).first()
    if entry is None:
        return _render_buffer(request, error="Entry not found")
    try:
        undo(entry, request.user)
    except ValidationError as e:
        return _render_buffer(request, error=e.messages[0] if e.messages else str(e))
    return _render_buffer(request, success="Undone")


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementSearch(request):
    if request.method == "GET":
        search = request.GET.get("search", "")
        if search == "":
            ra = Article.objects.none()
            rs = Storage.objects.none()
        else:
            ra = filter_by_search(Article.objects.all(), search, "base__name", "code__code")
            rs = filter_by_search(Storage.objects.all(), search, "name", "code__code")
        return render(request, "movement/searchResults.html", context={"resultsA": ra, "resultsS": rs})

    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def movementScanner(request, scannerId, state):
    if state == "toggle":
        active = request.POST.get("active_scanner", "")
        if active == scannerId:
            context = {"activeInput": "", "input": scannerId, "state": "off"}
        elif active == "":
            context = {"activeInput": "", "input": scannerId, "state": "on", "scan": True}
        else:
            context = {"activeInput": active, "input": scannerId, "state": "on", "scan": True}
        return render(request, "hub/modules/toggleScanner.html", context=context)

    return HttpResponseNotFound('<h1>Page not found</h1>')
