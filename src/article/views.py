from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from codeSystem.models import *
from .forms import *
from space.models import Space
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import csv
from storage.models import *
from tag.models import Tag
from movement.services import MovementService, resolve_space
from article.services import default_locations, composition_status, actual_quantity


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old

@login_required(login_url='/accounts/login/')
def article(request, typ, articleId):
    p = Article.objects.get(pk=articleId)
    if p.base.pType.name == typ:
        bpar = FormArticleBase(instance=p.base, prefix="base", article_type=p.base.pType)
        par = FormChangeArticle(instance=p, prefix="article", article_type=p.base.pType)

        context = {
            "symbol":p.base.pType.symbol,
            "searchFieldName":"articleSearch" + p.base.pType.name,
            "id":articleId,
            "modalId":"single",
            "actionType":"update",
            "form":[bpar,par],
            "typ":typ,
            "code":p.code.code if p.code else "",
            "link":("/a/" + p.code.code) if p.code else "",
            "storeActions":True,
            **_store_actions_context(p, "./%s/store" % articleId, "./%s/remove" % articleId),
            "tagChips":True,
            "tags":p.tags.all(),
            "allTags":Tag.objects.all(),
            "tagAddUrl":"./%s/tags/add" % articleId,
            "tagRemoveUrl":"./%s/tags/remove" % articleId,
        }
        if p.space and p.space.active:
            context.update(composition_context(p.space))
        return render(request, "hub/modules/item.html", context=context)
    else:
        return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.base.pType.name)

@login_required(login_url='/accounts/login/')
def addModal(request, typ):
    t = ArticleType.objects.get(name__exact=typ)
    context = {
        "modalId":"add",
        "form":[FormArticleBase(prefix="base", article_type=t), FormArticle(prefix="article", article_type=t)],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
def delModal(request, typ):
    context = {
        "modalId":"del",
        "form":[FormArticle()],
        "actionType":"del",
    }
    return render(request, "hub/modules/delForm.html", context=context)

@login_required(login_url='/accounts/login/')
def articleIncert(request, typ, articleId):
    try:
        p = Article.objects.get(pk=articleId)
        if p.base.pType.name == typ:
            par = FormChangeArticle(instance=p, article_type=p.base.pType)
            context = {
                "symbol":p.base.pType.symbol,
                "searchFieldName":"articleSearch" + p.base.pType.name,
                "id":articleId,
                "modalId":"single",
                "form":[par],
                "actionType":"update",
                "typ":typ,
            }
            return render(request, "hub/modules/itemForm.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.base.pType.name)
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def articles(request, typ):
    t = ArticleType.objects.get(name__exact=typ)

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        context={
            "symbol":t.symbol,
            "searchFieldName":"articleSearch" + t.name,
            'type':"article",
            "name":typ,
            "form":[FormArticleBase(prefix="base", article_type=t), FormArticle(prefix="article", article_type=t)],
            "typ":typ,
            "add":True,
            "del":True,
            "export":True,
            "qr":True,
        }
        return render(request, "hub/modules/items.html", context=context)

@login_required(login_url='/accounts/login/')
def addArticle(request, typ):
    t = ArticleType.objects.get(name__exact=typ)
    
    if t == None:
        context = {
                "toastName":"Error",
                "toastId":"errorToast",
                "toastText":"no article type named " + typ,
                "toastType":"alert"
            }
        return render(request, "hub/modules/toast.html", context=context)

    else:
        if request.method == "POST":
            pb = FormArticleBase(request.POST, prefix="base", article_type=t)
            p = FormArticle(request.POST, prefix="article", article_type=t)

            # resolve the optional target before creating anything
            target = None
            if p["stored"].value():
                try:
                    target = resolve_space(p["stored"].value())
                except ValidationError as e:
                    context = {
                        "toastName":"Error",
                        "toastId":"errorToast",
                        "toastText":e.messages[0] if e.messages else str(e),
                        "toastType":"alert"
                    }
                    return render(request, "hub/modules/toast.html", context=context)

            if pb.is_valid():
                base = pb.save(commit=False)
                base.pType = t
                base.save()
            else:
                context = {
                    "toastName":"Error",
                    "toastId":"errorToast",
                    "toastText":"article base not valid"+str(pb.errors),
                    "toastType":"alert"
                }
                return render(request, "hub/modules/toast.html", context=context)

            if p.is_valid():
                pa = p.save(commit=False)
                if p["code"].value() != "":
                    try:
                        code = UuidCode.objects.get(code=str(p["code"].value()))
                        if code.used:
                            context = {
                                "toastName":"Error",
                                "toastId":"errorToast",
                                "toastText":"code is already used",
                                "toastType":"alert"
                            }
                            return render(request, "hub/modules/toast.html", context=context)
                    except:
                        context = {
                            "toastName":"Error",
                            "toastId":"errorToast",
                            "toastText":"no code with id " + p["code"].value(),
                            "toastType":"alert"
                        }
                        return render(request, "hub/modules/toast.html", context=context)


                if p["code"].value() != "":
                    code.used = True
                    code.save()
                    pa.code = code

                pa.pType = t
                space = Space()
                if t.article_toggle_space:
                    space.active = True
                else:
                    space.active = False
                space.prefix = "a0"
                space.save()
                pa.space = space
                pa.base = base


                pa.save()

                if target is not None:
                    MovementService.store_article(pa, target, request.user)

                context = {
                    "toastName":"Add Succses",
                    "toastId":"successToast",
                    "toastText":pa.base.name + " was added to your system.",
                    "toastType":"status"
                }

                return render(request, "hub/modules/itemAdd.html", context=context)

        context = {
                "toastName":"Error",
                "toastId":"errorToast",
                "toastText":"article not valid " + str(p.errors),
                "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)

@login_required(login_url='/accounts/login/')
def delArticle(request, typ):
    t = ArticleType.objects.get(name__exact=typ)
    
    if t == None:
        context = {
                "toastName":"Error",
                "toastId":"errorToast",
                "toastText":"no article type named " + typ,
                "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)
    else:
        if request.method == "POST":
            delList = []
            delListReturn = ""
            for key, value in request.POST.items():
                if key.startswith("_"):
                    try:
                        pa = Article.objects.filter(base__pType__name__exact=typ, pk=value).first()
                        delList.append(pa)
                    except Exception as e:
                        context = {
                            "toastName":"Error",
                            "toastId":"errorToast",
                            "toastText":e,
                            "toastType":"alert"
                        }
                        return render(request, "hub/modules/toast.html", context=context)
            for i in delList:
                delListReturn = delListReturn + i.__str__() + " "
                i.delete()

            context = {
                "toastName":"Delete",
                "toastId":"successToast",
                "toastText":delListReturn,
                "toastType":"status"
            }
            return render(request, "hub/modules/itemDelete.html", context=context)

        context = {
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)

@login_required(login_url='/accounts/login/')
def updateArticle(request, typ, articleId):
    articleTypeObject = ArticleType.objects.get(name__exact=typ)
    articleObject = Article.objects.get(pk=articleId)

    if articleTypeObject == None:
        context = {
            toastName:"Error",
            toastId:"toastError",
            toastText:"no article type named " + typ,
            toastType:"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)
    else:
        if request.method == "POST":
            articleBaseForm = FormArticleBase(request.POST, instance=articleObject.base, prefix="base", article_type=articleTypeObject)
            articleForm =  FormChangeArticle(request.POST, instance=articleObject, prefix="article", article_type=articleTypeObject)

            if articleBaseForm.is_valid():
                articleBaseForm.save()
            else:
                context = {
                    "toastName":"Error",
                    "toastId":"errorToast",
                    "toastText":articleBaseForm.errors,
                    "toastType":"alert"
                }
                return render(request, "hub/modules/toast.html", context=context)

            if articleForm.is_valid():
                article = articleForm.save(commit=False)
                if article.menge == 0:
                    # menge 0 means "used up" (§4d)
                    article.delete()
                    context = {
                        "toastName":"Delete",
                        "toastId":"successToast",
                        "toastText":"article was deleted (menge 0)",
                        "toastType":"status"
                    }
                    return render(request, "hub/modules/toast.html", context=context)
                article.save()

            context = {
                "toastName":"Update",
                "toastId":"successToast",
                "toastText":"article was updated",
                "toastType":"status"
            }
            return render(request, "hub/modules/toast.html", context=context)
        context = {
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)

def _store_actions_context(article, storeUrl, removeUrl, error="", warning="", forceCode=""):
    return {
        "location": article.stored,
        "storeUrl": storeUrl,
        "removeUrl": removeUrl,
        "storeError": error,
        "storeWarning": warning,
        "forceCode": forceCode,
        "mergeable": article.base.pType.allow_merge_split,
        "defaultLocations": default_locations(article.base),
        "storeDefaultUrl": "./%s/store-default" % article.pk,
    }


@login_required(login_url='/accounts/login/')
def storeArticle(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    storeUrl = "./%s/store" % articleId
    removeUrl = "./%s/remove" % articleId
    if request.method == "POST":
        code = request.POST.get("code", "")
        try:
            target = resolve_space(code)
            warning = composition_warning(target, article)
            if warning and not request.POST.get("force"):
                return render(request, "hub/modules/storeActions.html",
                              context=_store_actions_context(article, storeUrl, removeUrl,
                                                             warning=warning, forceCode=code))
            amount = _int_or_none(request.POST.get("amount"))
            MovementService.store_article(article, target, request.user, amount=amount)
            error = ""
        except ValidationError as e:
            error = e.messages[0] if e.messages else str(e)
        return render(request, "hub/modules/storeActions.html",
                      context=_store_actions_context(article, storeUrl, removeUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
def removeArticle(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    storeUrl = "./%s/store" % articleId
    removeUrl = "./%s/remove" % articleId
    if request.method == "POST":
        MovementService.remove_article(article, request.user)
        return render(request, "hub/modules/storeActions.html",
                      context=_store_actions_context(article, storeUrl, removeUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
def storeToDefault(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    storeUrl = "./%s/store" % articleId
    removeUrl = "./%s/remove" % articleId
    if request.method == "POST":
        targets = default_locations(article.base)
        if not targets:
            error = "No default location"
        else:
            try:
                MovementService.store_article(article, targets[0], request.user)
                error = ""
            except ValidationError as e:
                error = e.messages[0] if e.messages else str(e)
        if request.POST.get("next"):
            return redirect(request.POST["next"])
        return render(request, "hub/modules/storeActions.html",
                      context=_store_actions_context(article, storeUrl, removeUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


def _tag_chips_context(obj, tagAddUrl, tagRemoveUrl, error=""):
    return {
        "tags": obj.tags.all(),
        "allTags": Tag.objects.all(),
        "tagAddUrl": tagAddUrl,
        "tagRemoveUrl": tagRemoveUrl,
        "tagError": error,
    }


@login_required(login_url='/accounts/login/')
def addArticleTag(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    tagAddUrl = "./%s/tags/add" % articleId
    tagRemoveUrl = "./%s/tags/remove" % articleId
    if request.method == "POST":
        name = request.POST.get("tag", "").strip()
        tag = Tag.objects.filter(name__iexact=name).first()
        if tag is None:
            error = "No tag named %s" % name
        else:
            article.tags.add(tag)
            error = ""
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(article, tagAddUrl, tagRemoveUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
def removeArticleTag(request, typ, articleId, tagId):
    article = Article.objects.get(pk=articleId)
    tagAddUrl = "./%s/tags/add" % articleId
    tagRemoveUrl = "./%s/tags/remove" % articleId
    if request.method == "POST":
        article.tags.remove(Tag.objects.get(pk=tagId))
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(article, tagAddUrl, tagRemoveUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


def _int_or_none(value):
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def composition_context(space, error="", warning="", forceBase="", forceSoll="", forceMin=""):
    """Context for the composition editor (§4d)."""
    return {
        "showComposition": True,
        "compositionStatus": composition_status(space),
        "compositionAddUrl": "/composition/%s/add" % space.pk,
        "compositionRemoveUrl": "/composition/%s/remove" % space.pk,
        "compositionError": error,
        "compositionWarning": warning,
        "forceBase": forceBase,
        "forceSoll": forceSoll,
        "forceMin": forceMin,
        "allBases": ArticleBase.objects.all(),
    }


def composition_warning(target_space, article):
    """Warning when the target already holds enough of the article's base (§4d)."""
    item = CompositionItem.objects.filter(space=target_space, base=article.base).first()
    if item is None or item.soll_menge is None:
        return ""
    ist = actual_quantity(target_space, article.base)
    if ist >= item.soll_menge:
        return "Already enough %s here (Soll %s / Ist %s)" % (article.base.name, item.soll_menge, ist)
    return ""


def _allocation_warning(base, soll, space):
    """Warning when setting ``soll`` for ``base`` over-commits the articles (§4d)."""
    if soll is None:
        return ""
    others = CompositionItem.objects.filter(base=base).exclude(space=space)
    total = sum(item.soll_menge or 0 for item in others) + soll
    available = Article.objects.filter(base=base).count()
    if total > available:
        return "Only %s %s available, but %s allocated" % (available, base.name, total)
    return ""


@login_required(login_url='/accounts/login/')
def addCompositionItem(request, spaceId):
    space = Space.objects.get(pk=spaceId)
    if request.method == "POST":
        name = request.POST.get("base", "").strip()
        base = ArticleBase.objects.filter(name__iexact=name).first()
        error = ""
        if base is None:
            error = "No article base named %s" % name
        else:
            soll = _int_or_none(request.POST.get("soll"))
            min_ = _int_or_none(request.POST.get("min"))
            warning = _allocation_warning(base, soll, space)
            if warning and not request.POST.get("force"):
                return render(request, "hub/modules/composition.html",
                              context=composition_context(
                                  space, warning=warning, forceBase=name,
                                  forceSoll=request.POST.get("soll", ""),
                                  forceMin=request.POST.get("min", "")))
            CompositionItem.objects.update_or_create(
                space=space, base=base,
                defaults={"soll_menge": soll, "mindestmenge": min_})
        return render(request, "hub/modules/composition.html",
                      context=composition_context(space, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
def removeCompositionItem(request, spaceId, itemId):
    space = Space.objects.get(pk=spaceId)
    if request.method == "POST":
        CompositionItem.objects.filter(pk=itemId, space=space).delete()
        return render(request, "hub/modules/composition.html",
                      context=composition_context(space))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
def searchArticle(request, typ):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = Article.objects.filter(base__pType__name__exact=typ)
        else:
            r = Article.objects.filter(Q(base__name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), base__pType__name__exact=typ)
        return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})

@login_required(login_url='/accounts/login/')
def exportArticles(request, typ):
    response = HttpResponse(content_type='text/csv; charset=iso-8859-1')
    response['Content-Disposition'] = 'attachment; filename="articles.csv"'

    thereIsOne = False

    writer = csv.writer(response, dialect="excel")
    writer.writerow(['name', 'code', 'type'])
    for key, value in request.POST.items():
        if key.startswith("_"):
            article = Article.objects.get(pk=value)
            if article.base.pType.name == typ:
                thereIsOne = True
                writer.writerow([article.base.name, article.code.code, article.base.pType.name])
    return response

@login_required(login_url='/accounts/login/')
def articleScanner(request, typ, scannerId, state):
    if state == "toggle":
        print(request.POST)
        if request.POST["active_scanner"] == scannerId:
            context = {
                "activeInput":"",
                "input":scannerId,
                "state":"off",
            }
            return render(request, "hub/modules/toggleScanner.html", context=context)
        elif request.POST["active_scanner"] == "":
            context = {
                "activeInput":"",
                "input":scannerId,
                "state":"on",
            }
        else:
            context = {
                "activeInput":request.POST["active_scanner"],
                "input":scannerId,
                "state":"on",
            }
        return render(request, "hub/modules/toggleScanner.html", context=context)


    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

