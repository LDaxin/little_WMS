from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from decimal import Decimal, InvalidOperation
from .models import *
from codeSystem.models import *
from .forms import *
from space.models import Space
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from organisation.decorators import require_perm, require_scope
from organisation.permissions import has_scope, is_assigned_only
from organisation.services import active_organisation
from django.db.models import Q
import csv
from storage.models import *
from tag.models import Tag
from movement.services import MovementService, resolve_space
from article.services import default_locations, composition_status, actual_quantity, location_minimum_sum
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from audit.models import AuditLog
from audit.services import log as audit_log


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old


def _can_article(request, action, article):
    """Scope check for a specific article (§3)."""
    return has_scope(request.user, "article", action, active_organisation(request), article)


def _require_article(request, action, article):
    if not _can_article(request, action, article):
        raise PermissionDenied


def _scoped_articles(qs, request):
    """Filter to assigned articles for `_assigned`-only users (§3)."""
    if is_assigned_only(request.user, "article", "view", active_organisation(request)):
        qs = qs.filter(assigned_to=request.user)
    return qs


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def article(request, typ, articleId):
    p = Article.objects.get(pk=articleId)
    _require_article(request, "view", p)
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
            "assignedTo":True,
            "assignees":p.assigned_to.all(),
            "allUsers":User.objects.all(),
            "assignUrl":"./%s/assign" % articleId,
            "unassignUrl":"./%s/unassign" % articleId,
            "auditTimeline":True,
            "auditLogs":AuditLog.objects.filter(
                content_type=ContentType.objects.get_for_model(Article),
                object_id=p.pk)[:20],
        }
        if p.space and p.space.active:
            context.update(composition_context(p.space))
        return render(request, "hub/modules/item.html", context=context)
    else:
        return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.base.pType.name)

@login_required(login_url='/accounts/login/')
@require_scope("article", "create")
def addModal(request, typ):
    t = ArticleType.objects.get(name__exact=typ)
    context = {
        "modalId":"add",
        "form":[FormArticleBase(prefix="base", article_type=t), FormArticle(prefix="article", article_type=t)],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_scope("article", "delete")
def delModal(request, typ):
    context = {
        "modalId":"del",
        "form":[FormArticle()],
        "actionType":"del",
    }
    return render(request, "hub/modules/delForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def articleIncert(request, typ, articleId):
    p = Article.objects.filter(pk=articleId).first()
    if p is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    _require_article(request, "edit", p)
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
    return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.base.pType.name)

@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
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
@require_scope("article", "create")
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

                # quantity lives on Stock; start "not stored" (stored=None)
                Stock.objects.create(
                    article=pa, stored=None, menge=_decimal(p.cleaned_data.get("menge")) or 1
                )
                audit_log("created", pa, request.user, {"name": base.name})

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
@require_scope("article", "delete")
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
                _require_article(request, "delete", i)
                delListReturn = delListReturn + i.__str__() + " "
                audit_log("deleted", i, request.user)
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
@require_scope("article", "edit")
def updateArticle(request, typ, articleId):
    articleTypeObject = ArticleType.objects.get(name__exact=typ)
    articleObject = Article.objects.get(pk=articleId)
    _require_article(request, "edit", articleObject)

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
            old_values = _snapshot(articleObject)
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
                menge = _decimal(articleForm.cleaned_data.get("menge"))
                if menge is not None and menge <= 0:
                    # menge 0 means "used up" (§4d)
                    audit_log("deleted", article, request.user, {"reason": "menge 0"})
                    article.delete()
                    context = {
                        "toastName":"Delete",
                        "toastId":"successToast",
                        "toastText":"article was deleted (menge 0)",
                        "toastType":"status"
                    }
                    return render(request, "hub/modules/toast.html", context=context)
                article.save()
                audit_log("updated", article, request.user, _diff(old_values, _snapshot(article)))
                if menge is not None:
                    stock, _ = Stock.objects.get_or_create(
                        article=article, stored=None, defaults={"menge": menge})
                    stock.menge = menge
                    stock.save()

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
        "stocks": article.stocks.exclude(stored=None),
        "not_stored": sum(s.menge for s in article.stocks.filter(stored=None)),
        "storeUrl": storeUrl,
        "removeUrl": removeUrl,
        "storeSearchUrl": storeUrl + "-search",
        "storeError": error,
        "storeWarning": warning,
        "forceCode": forceCode,
        "mergeable": article.base.pType.allow_merge_split,
        "defaultLocations": default_locations(article.base),
        "storeDefaultUrl": "./%s/store-default" % article.pk,
    }


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def storeArticle(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "move", article)
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
@require_scope("article", "move")
def removeArticle(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "move", article)
    storeUrl = "./%s/store" % articleId
    removeUrl = "./%s/remove" % articleId
    if request.method == "POST":
        stock = Stock.objects.filter(pk=request.POST.get("stock"), article=article).first()
        MovementService.remove_article(
            article, space=stock.stored if stock else None, user=request.user)
        return render(request, "hub/modules/storeActions.html",
                      context=_store_actions_context(article, storeUrl, removeUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def storeToDefault(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "move", article)
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


@login_required(login_url='/accounts/login/')
@require_scope("article", "move")
def storeTargetSearch(request, typ, articleId):
    """Live suggestions for the store-target field (code or name, § code-input)."""
    query = request.GET.get("code", "").strip()
    if query:
        storages = Storage.objects.filter(
            Q(name__contains=query) | Q(code__code__contains=query)
        )[:10]
        containers = Article.objects.filter(
            Q(base__name__contains=query) | Q(code__code__contains=query),
            space__active=True,
        )[:10]
    else:
        storages = Storage.objects.none()
        containers = Article.objects.none()
    return render(request, "hub/modules/storeTargetResults.html", {
        "storages": storages,
        "containers": containers,
        "storeUrl": "./%s/store" % articleId,
    })


def _tag_chips_context(obj, tagAddUrl, tagRemoveUrl, error=""):
    return {
        "tags": obj.tags.all(),
        "allTags": Tag.objects.all(),
        "tagAddUrl": tagAddUrl,
        "tagRemoveUrl": tagRemoveUrl,
        "tagError": error,
    }


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def addArticleTag(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
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
@require_scope("article", "edit")
def removeArticleTag(request, typ, articleId, tagId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    tagAddUrl = "./%s/tags/add" % articleId
    tagRemoveUrl = "./%s/tags/remove" % articleId
    if request.method == "POST":
        article.tags.remove(Tag.objects.get(pk=tagId))
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(article, tagAddUrl, tagRemoveUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


def _assigned_context(article):
    return {
        "assignees": article.assigned_to.all(),
        "allUsers": User.objects.all(),
        "assignUrl": "./%s/assign" % article.pk,
        "unassignUrl": "./%s/unassign" % article.pk,
    }


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def assignArticle(request, typ, articleId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    if request.method == "POST":
        user = User.objects.filter(pk=request.POST.get("user")).first()
        if user is not None:
            article.assigned_to.add(user)
    return render(request, "hub/modules/assignedTo.html", context=_assigned_context(article))


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def unassignArticle(request, typ, articleId, userId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    if request.method == "POST":
        user = User.objects.filter(pk=userId).first()
        if user is not None:
            article.assigned_to.remove(user)
    return render(request, "hub/modules/assignedTo.html", context=_assigned_context(article))


def _int_or_none(value):
    value = (value or "").strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _decimal(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _snapshot(obj):
    """Editable field values as strings, for change tracking (§32)."""
    return {k: (None if v is None else str(v)) for k, v in model_to_dict(obj).items()}


def _diff(old, new):
    return {k: {"old": old.get(k), "new": v} for k, v in new.items() if old.get(k) != v}


def composition_context(space, error="", warning="", forceBase="", forceSoll="", forceMin=""):
    """Context for the composition editor (§4d)."""
    return {
        "showComposition": True,
        "compositionStatus": composition_status(space),
        "compositionAddUrl": "/composition/%s/add" % space.pk,
        "compositionRemoveUrl": "/composition/%s/remove" % space.pk,
        "compositionGlobalUrl": "/composition/%s/set-global" % space.pk,
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
@require_perm("storage.edit_all")
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
@require_perm("storage.edit_all")
def removeCompositionItem(request, spaceId, itemId):
    space = Space.objects.get(pk=spaceId)
    if request.method == "POST":
        CompositionItem.objects.filter(pk=itemId, space=space).delete()
        return render(request, "hub/modules/composition.html",
                      context=composition_context(space))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def setGlobalMinimum(request, spaceId, itemId):
    """Set a base's global minimum to the sum of its per-location minimums (§4d)."""
    space = Space.objects.get(pk=spaceId)
    if request.method == "POST":
        item = CompositionItem.objects.filter(pk=itemId, space=space).first()
        if item is not None:
            item.base.mindestbestand = location_minimum_sum(item.base)
            item.base.save()
        return render(request, "hub/modules/composition.html",
                      context=composition_context(space))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def searchArticle(request, typ):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = Article.objects.filter(base__pType__name__exact=typ)
        else:
            r = Article.objects.filter(Q(base__name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), base__pType__name__exact=typ)
        r = _scoped_articles(r, request)
        return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})

@login_required(login_url='/accounts/login/')
@require_perm("export.csv_all")
def exportArticles(request, typ):
    response = HttpResponse(content_type='text/csv; charset=iso-8859-1')
    response['Content-Disposition'] = 'attachment; filename="articles.csv"'

    thereIsOne = False

    writer = csv.writer(response, dialect="excel")
    writer.writerow(['name', 'code', 'type'])
    assigned_only = is_assigned_only(request.user, "article", "view", active_organisation(request))
    for key, value in request.POST.items():
        if key.startswith("_"):
            article = Article.objects.get(pk=value)
            if assigned_only and request.user not in article.assigned_to.all():
                continue
            if article.base.pType.name == typ:
                thereIsOne = True
                writer.writerow([article.base.name, article.code.code, article.base.pType.name])
    return response

@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
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

