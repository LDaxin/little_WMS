from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q

from article.models import Article
from storage.models import Storage
from space.services import space_path
from movement.services import MovementService, resolve_space
from movement.session import get_state, save_state, reset
from article.services import default_locations

# Create your views here.


def _resolve_target(code):
    """The Storage/Article behind a target code, for display."""
    if not code:
        return None
    if code.startswith("s0"):
        return Storage.objects.filter(code__code=code).first()
    if code.startswith("a0"):
        return Article.objects.filter(code__code=code).first()
    return None


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
    return {
        "mode": state["mode"],
        "buffer": buffered,
        "target": _resolve_target(state["target"]),
        "target_smart": state["target_smart"],
        "error": error,
        "success": success,
    }


def _render_buffer(request, error="", success=""):
    return render(request, "movement/buffer.html",
                  context=_buffer_context(request, error=error, success=success))


@login_required(login_url='/accounts/login/')
def movement(request):
    return render(request, "movement/movement.html", context=_buffer_context(request))


@login_required(login_url='/accounts/login/')
def where(request):
    """'Where is...?' – current and default location of an article (§5b)."""
    query = request.GET.get("q", "").strip()
    article = None
    results = []
    if query:
        if query.startswith("a0"):
            article = Article.objects.filter(code__code=query).first()
        else:
            results = Article.objects.filter(
                Q(base__name__contains=query) | Q(code__code__contains=query)
            )[:20]

    context = {
        "query": query,
        "article": article,
        "results": results,
        "current_path": space_path(article.stored) if article else "",
        "default_paths": [space_path(loc) for loc in default_locations(article.base)] if article else [],
    }
    return render(request, "movement/where.html", context=context)


@login_required(login_url='/accounts/login/')
def whereSearch(request):
    search = request.GET.get("q", "").strip()
    results = []
    if search:
        results = Article.objects.filter(
            Q(base__name__contains=search) | Q(code__code__contains=search)
        )[:20]
    return render(request, "movement/whereResults.html", context={"results": results})


@login_required(login_url='/accounts/login/')
def movementScan(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    code = request.POST.get("code", "").strip()
    error = ""
    try:
        if code.startswith("s0"):
            Storage.objects.get(code__code=code)
            state["target"] = code
            state["target_smart"] = False
        elif code.startswith("a0"):
            article = Article.objects.get(code__code=code)
            if article.space and article.space.active and not state["target"]:
                # smart default: a container becomes the target
                state["target"] = code
                state["target_smart"] = True
            elif code not in state["buffer"]:
                state["buffer"].append(code)
        else:
            raise ValidationError("Unknown code %s" % code)
    except (Storage.DoesNotExist, Article.DoesNotExist):
        error = "No object with code %s" % code
    except ValidationError as e:
        error = e.messages[0] if e.messages else str(e)

    save_state(request.session, state)
    return _render_buffer(request, error=error)


@login_required(login_url='/accounts/login/')
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
def movementClear(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    reset(request.session)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
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
def movementTargetClear(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    state["target"] = None
    state["target_smart"] = False
    save_state(request.session, state)
    return _render_buffer(request)


@login_required(login_url='/accounts/login/')
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
def movementStore(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    try:
        target = resolve_space(state["target"] or "")
        articles = _articles_from_codes(state["buffer"])
        MovementService.store_articles(articles, target, request.user)
    except ValidationError as e:
        return _render_buffer(request, error=e.messages[0] if e.messages else str(e))

    count = len(articles)
    reset(request.session)
    return _render_buffer(request, success="Stored %s article(s)" % count)


@login_required(login_url='/accounts/login/')
def movementRemove(request):
    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')

    state = get_state(request.session)
    try:
        articles = _articles_from_codes(state["buffer"])
        for article in articles:
            MovementService.remove_article(article, request.user)
    except ValidationError as e:
        return _render_buffer(request, error=e.messages[0] if e.messages else str(e))

    count = len(articles)
    reset(request.session)
    return _render_buffer(request, success="Removed %s article(s)" % count)


@login_required(login_url='/accounts/login/')
def movementSearch(request):
    if request.method == "GET":
        search = request.GET.get("search", "")
        if search == "":
            ra = Article.objects.none()
            rs = Storage.objects.none()
        else:
            ra = Article.objects.filter(Q(base__name__contains=search) | Q(code__code__contains=search))
            rs = Storage.objects.filter(Q(name__contains=search) | Q(code__code__contains=search))
        return render(request, "movement/searchResults.html", context={"resultsA": ra, "resultsS": rs})

    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
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
