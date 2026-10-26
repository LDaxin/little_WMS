from django.shortcuts import render
from django.template.loader import render_to_string
from storage.models import Storage
from article.models import Article
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import Q

from movement.services import MovementService, resolve_space

# Create your views here.


def _toast(request, name, text, toast_type, toast_id):
    return render(request, "hub/modules/toast.html", context={
        "toastName": name, "toastId": toast_id, "toastText": text, "toastType": toast_type,
    })


def _error_toast(request, text):
    return _toast(request, "Error", text, "alert", "errorToast")


def _success_toast(request, text):
    return _toast(request, "Success", text, "success", "successToast")


def _json_error(message):
    return JsonResponse({
        "error": message,
        "errorToast": render_to_string("hub/modules/toast.html", context={
            "toastName": "Error", "toastId": "errorToast", "toastText": message, "toastType": "alert",
        }),
    })


def _articles_from_post(request):
    """Collect the buffered articles from the ``articleCode*`` POST fields."""
    articles = []
    for key, value in request.POST.items():
        if key.startswith("articleCode"):
            try:
                articles.append(Article.objects.get(code__code=value))
            except Article.DoesNotExist:
                raise ValidationError("No article with code %s" % value)
    return articles


@login_required(login_url='/accounts/login/')
def movement(request):

    return render(request, "movement/movement.html")


@login_required(login_url='/accounts/login/')
def movementRemove(request):
    if request.method == "POST":
        try:
            articles = _articles_from_post(request)
            for article in articles:
                MovementService.remove_article(article, request.user)
        except ValidationError as e:
            return _error_toast(request, e.messages[0] if e.messages else str(e))
        return _success_toast(request, "Removed %s article(s)" % len(articles))

    return _error_toast(request, "what are you trying to do")


@login_required(login_url='/accounts/login/')
def movementStore(request):
    if request.method == "POST":
        try:
            target = resolve_space(request.POST.get("storageCode", ""))
            articles = _articles_from_post(request)
            MovementService.store_articles(articles, target, request.user)
        except ValidationError as e:
            return _error_toast(request, e.messages[0] if e.messages else str(e))
        return _success_toast(request, "Stored %s article(s)" % len(articles))

    return _error_toast(request, "what are you trying to do")


@login_required(login_url='/accounts/login/')
def movementCodeInfo(request):
    if request.method == "GET":
        code = request.GET.get("code", "")
        if code.startswith("a0"):
            try:
                article = Article.objects.get(code__code=code)
            except Article.DoesNotExist:
                return _json_error("no such a article in the System")

            return JsonResponse({
                "error": "",
                "name": article.base.name,
                "code": article.code.code,
                "storable": True,
                "storage": False,
                "space": article.space.active if article.space else False,
            })

        elif code.startswith("s0"):
            try:
                storage = Storage.objects.get(code__code=code)
            except Storage.DoesNotExist:
                return _json_error("no such a storage in the System")

            return JsonResponse({
                "error": "",
                "name": storage.name,
                "code": storage.code.code,
                "storable": False,
                "storage": True,
                "space": True,
            })

        return _json_error("not a valide code")

    return _json_error("what are you trying to do?")


@login_required(login_url='/accounts/login/')
def movementSearch(request):
    if request.method == "GET":
        search = request.GET.get("search", "")
        if search == "":
            ra = Article.objects.filter(base__name__exact="")
            rs = Storage.objects.filter(name__exact="")
        else:
            ra = Article.objects.filter(Q(base__name__contains=search) | Q(code__code__contains=search))
            rs = Storage.objects.filter(Q(name__contains=search) | Q(code__code__contains=search))
        return render(request, "hub/modules/quickResults.html", context={"resultsA": ra, "resultsS": rs})

    return _json_error("what are you trying to do?")
