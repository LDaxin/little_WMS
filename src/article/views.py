from django.utils.translation import gettext as _
from hub.toasts import toast
from hub.csv import csv_response
from hub.search import filter_by_search
from hub.columns import default_columns, order_by, resolve_view_mode, selected_columns
from hub.columns import columns as all_columns
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.urls import reverse
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
from organisation.services import active_organisation, active_profile
from storage.models import *
from tag.models import Tag
from movement.services import MovementService, resolve_space
from article.services import default_locations, composition_status, actual_quantity, location_minimum_sum
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict
from audit.models import AuditLog
from audit.services import log as audit_log
from django.core.paginator import Paginator
from django.db.models import Count, Sum

PAGE_SIZE = 50


def _article_terms(article):
    """The article's dated terms for the mini calendar (§2)."""
    from occasion.models import Packlist

    terms = []
    for entry in Packlist.objects.filter(article=article).select_related("occasion__calendar_entry"):
        calendar_entry = entry.occasion.calendar_entry
        terms.append({
            "date": calendar_entry.start_date,
            "label": "Occasion: %s" % calendar_entry.title,
            "url": reverse("occasion", args=[entry.occasion.pk]),
        })
    if article.ablaufdatum:
        terms.append({"date": article.ablaufdatum, "label": "Expires", "url": None})
    for entry in article.calendar_entries.filter(entry_type="maintenance"):
        terms.append({"date": entry.start_date, "label": "Maintenance: %s" % entry.title, "url": None})
    for entry in article.calendar_entries.filter(entry_type="loan"):
        terms.append({"date": entry.start_date, "label": entry.title, "url": None})
    terms.sort(key=lambda term: term["date"])
    return terms


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
            "version":p.version,
            "storeActions":True,
            "articleCalendar":True,
            "articleTerms":_article_terms(p),
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
            "imageGallery":True,
            "images":p.images.all(),
            "imageBaseUrl":"./%s/images/" % articleId,
        }
        if p.space and p.space.active:
            context.update(composition_context(p.space))
        return render(request, "hub/modules/item.html", context=context)
    else:
        return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.base.pType.name)


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def addArticleImage(request, typ, articleId):
    """Upload an image to an article (§15)."""
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    if request.method == "POST" and request.FILES.get("image"):
        ArticleImage.objects.create(
            article=article,
            image=request.FILES["image"],
            caption=request.POST.get("caption", ""),
            is_primary=not article.images.exists(),
        )
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def deleteArticleImage(request, typ, articleId, imageId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    if request.method == "POST":
        image = article.images.filter(pk=imageId).first()
        if image:
            image.delete()
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def setPrimaryArticleImage(request, typ, articleId, imageId):
    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    if request.method == "POST":
        article.images.update(is_primary=False)
        article.images.filter(pk=imageId).update(is_primary=True)
    return redirect("article", typ=typ, articleId=articleId)


@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def addMaintenance(request, typ, articleId):
    """Record a maintenance due date for an article (§2)."""
    from planning.models import CalendarEntry

    article = Article.objects.get(pk=articleId)
    _require_article(request, "edit", article)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        due = request.POST.get("due_date", "")
        if title and due:
            CalendarEntry.objects.create(
                entry_type="maintenance",
                title=title,
                start_date=due,
                article=article,
                responsible_user=request.user,
            )
    return redirect("article", typ=typ, articleId=articleId)

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
            "list_type":"article",
            "available_columns": all_columns("article"),
            "columns": selected_columns("article", request.GET.get("cols"), active_profile(request)),
            "cols": request.GET.get("cols", ""),
            "list_view_mode": resolve_view_mode(request),
            "sort": request.GET.get("sort", ""),
            "name":typ,
            "form":[FormArticleBase(prefix="base", article_type=t), FormArticle(prefix="article", article_type=t)],
            "typ":typ,
            "add":True,
            "del":True,
            "export":True,
            "qr":True,
        }
        view_id = request.GET.get("view")
        if view_id:
            import json

            from savedviews.views import visible_views

            saved_view = visible_views(request.user).filter(pk=view_id).first()
            if saved_view:
                context["savedQuery"] = json.dumps(saved_view.query)
        return render(request, "hub/modules/items.html", context=context)


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def articlesAll(request):
    """List all articles across types."""
    return render(request, "hub/modules/items.html", context={
        "symbol": "Logo",
        "searchFieldName": "articleSearchAll",
        "type": "article",
        "list_type": "article",
        "available_columns": all_columns("article"),
        "columns": selected_columns("article", request.GET.get("cols"), active_profile(request)),
        "cols": request.GET.get("cols", ""),
        "list_view_mode": resolve_view_mode(request),
        "sort": request.GET.get("sort", ""),
        "name": "",
        "form": [],
        "typ": "",
        "show_type": True,
        "add": False,
        "del": False,
        "export": False,
        "qr": False,
    })


def _article_stocks(request, params=None):
    """The filtered, sorted stock queryset for the article list (§ list-views).

    ``params`` defaults to the query string; bulk actions pass their POST data
    so "select all matches" re-runs the same filter server-side.
    """
    from querybuilder.services import ARTICLE_FIELDS, QueryError, parse_json

    params = request.GET if params is None else params
    stocks = Stock.objects.select_related("article__base__pType", "article__code", "stored")
    query = params.get("query")
    if query:
        try:
            stocks = stocks.filter(parse_json(query, ARTICLE_FIELDS, prefix="article__"))
        except QueryError:
            pass
    else:
        stocks = filter_by_search(
            stocks, params.get("search", ""), "article__base__name", "article__code__code"
        )
    if is_assigned_only(request.user, "article", "view", active_organisation(request)):
        stocks = stocks.filter(article__assigned_to=request.user)
    return order_by(stocks, "article", params.get("sort", ""))


def _selected_articles(request, typ):
    """The articles a bulk action applies to (§ list-views).

    With ``all`` in the POST the current filter is re-run server-side (all
    matches, not only the loaded rows); otherwise the explicit ``_<id>`` values.
    """
    if request.POST.get("all"):
        ids = _article_stocks(request, request.POST).filter(
            article__base__pType__name__exact=typ
        ).values_list("article_id", flat=True)
        return Article.objects.filter(pk__in=list(ids))
    ids = [value for key, value in request.POST.items() if key.startswith("_")]
    articles = Article.objects.filter(pk__in=ids, base__pType__name__exact=typ)
    if is_assigned_only(request.user, "article", "view", active_organisation(request)):
        articles = articles.filter(assigned_to=request.user)
    return articles


def _article_groups(stocks, totals, counts):
    """Group stock rows by article for the list (§ list-views)."""
    groups = []
    by_article = {}
    for stock in stocks:
        article = stock.article
        group = by_article.get(article.pk)
        if group is None:
            group = {"article": article, "rows": [], "total": totals.get(article.pk, 0)}
            by_article[article.pk] = group
            groups.append(group)
        group["rows"].append(stock)
    for group in groups:
        group["shown"] = len(group["rows"])
        group["total_locations"] = counts.get(group["article"].pk, group["shown"])
        group["partial"] = group["shown"] < group["total_locations"]
    return groups


def _article_list_context(request, stocks, search_field):
    """The list context for the article stock list (§ list-views)."""
    totals = dict(stocks.order_by().values_list("article_id").annotate(total=Sum("menge")))
    counts = dict(stocks.order_by().values_list("article_id").annotate(n=Count("id")))
    page = Paginator(stocks, PAGE_SIZE).get_page(request.GET.get("page"))
    cols = request.GET.get("cols", "")
    sort = request.GET.get("sort", "")
    return {
        "list_type": "article",
        "columns": selected_columns("article", cols, active_profile(request)),
        "groups": _article_groups(page.object_list, totals, counts),
        "rows": page.object_list,
        "flat": sort.lstrip("-") == "quantity",
        "selectable": True,
        "sort": sort,
        "cols": cols,
        "list_view_mode": resolve_view_mode(request),
        "searchFieldName": search_field,
        "page": page,
    }


@login_required(login_url='/accounts/login/')
@require_scope("article", "view")
def searchArticlesAll(request):
    if request.method == "GET":
        context = _article_list_context(request, _article_stocks(request), "articleSearchAll")
        template = "hub/modules/listAppend.html" if request.GET.get("append") else "hub/modules/list.html"
        return render(request, template, context=context)


@login_required(login_url='/accounts/login/')
@require_scope("article", "create")
def addArticle(request, typ):
    t = ArticleType.objects.get(name__exact=typ)
    
    if t == None:
        return toast(request, _("Error"), _("no article type named ") + typ, "alert")

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
                    return toast(request, "Error", e.messages[0] if e.messages else str(e), "alert")

            if pb.is_valid():
                base = pb.save(commit=False)
                base.pType = t
                base.save()
            else:
                return toast(request, _("Error"), _("article base not valid")+str(pb.errors), "alert")

            if p.is_valid():
                pa = p.save(commit=False)
                if p["code"].value() != "":
                    try:
                        code = UuidCode.objects.get(code=str(p["code"].value()))
                        if code.used:
                            return toast(request, _("Error"), _("code is already used"), "alert")
                    except:
                        return toast(request, _("Error"), _("no code with id ") + p["code"].value(), "alert")


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

                return toast(request, "Add Succses", pa.base.name + " was added to your system.", "status", template="hub/modules/itemAdd.html")

        return toast(request, _("Error"), _("article not valid ") + str(p.errors), "alert")

@login_required(login_url='/accounts/login/')
@require_scope("article", "delete")
def delArticle(request, typ):
    t = ArticleType.objects.get(name__exact=typ)
    
    if t == None:
        return toast(request, _("Error"), _("no article type named ") + typ, "alert")
    else:
        if request.method == "POST":
            delListReturn = ""
            for i in list(_selected_articles(request, typ)):
                _require_article(request, "delete", i)
                delListReturn = delListReturn + i.__str__() + " "
                audit_log("deleted", i, request.user)
                i.delete()

            return toast(request, "Delete", delListReturn, "status", template="hub/modules/itemDelete.html")

        return toast(request, _("Error"), _("something went wrong"), "alert")

@login_required(login_url='/accounts/login/')
@require_scope("article", "edit")
def updateArticle(request, typ, articleId):
    articleTypeObject = ArticleType.objects.get(name__exact=typ)
    articleObject = Article.objects.get(pk=articleId)
    _require_article(request, "edit", articleObject)

    if articleTypeObject == None:
        return toast(request, _("Error"), _("no article type named ") + typ, "alert")
    else:
        if request.method == "POST":
            loaded_version = request.POST.get("version")
            if loaded_version is not None and loaded_version.isdigit() and int(loaded_version) != articleObject.version:
                return toast(request, _("Error"), _("The article was changed by someone else. Please reload."), "alert")
            old_values = _snapshot(articleObject)
            articleBaseForm = FormArticleBase(request.POST, instance=articleObject.base, prefix="base", article_type=articleTypeObject)
            articleForm =  FormChangeArticle(request.POST, instance=articleObject, prefix="article", article_type=articleTypeObject)

            if articleBaseForm.is_valid():
                articleBaseForm.save()
            else:
                return toast(request, "Error", articleBaseForm.errors, "alert")

            if articleForm.is_valid():
                article = articleForm.save(commit=False)
                menge = _decimal(articleForm.cleaned_data.get("menge"))
                if menge is not None and menge <= 0:
                    # menge 0 means "used up" (§4d)
                    audit_log("deleted", article, request.user, {"reason": "menge 0"})
                    article.delete()
                    return toast(request, _("Delete"), _("article was deleted (menge 0)"), "status")
                article.save()
                article.version += 1
                article.save(update_fields=["version"])
                audit_log("updated", article, request.user, _diff(old_values, _snapshot(article)))
                if menge is not None:
                    stock, _created = Stock.objects.get_or_create(
                        article=article, stored=None, defaults={"menge": menge})
                    stock.menge = menge
                    stock.save()

            return toast(request, _("Update"), _("article was updated"), "status")
        return toast(request, _("Error"), _("something went wrong"), "alert")

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
        storages = filter_by_search(Storage.objects.all(), query, "name", "code__code")[:10]
        containers = filter_by_search(
            Article.objects.filter(space__active=True), query, "base__name", "code__code"
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
        stocks = _article_stocks(request).filter(article__base__pType__name__exact=typ)
        context = _article_list_context(request, stocks, "articleSearch" + typ)
        template = "hub/modules/listAppend.html" if request.GET.get("append") else "hub/modules/list.html"
        return render(request, template, context=context)

@login_required(login_url='/accounts/login/')
@require_perm("export.csv_all")
def exportArticles(request, typ):
    rows = [
        [article.base.name, article.code.code, article.base.pType.name]
        for article in _selected_articles(request, typ)
    ]
    return csv_response("articles.csv", ["name", "code", "type"], rows, encoding="iso-8859-1")

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


@login_required(login_url='/accounts/login/')
@require_perm("article.create_all")
def importArticles(request):
    """Upload a CSV and preview the import (§19)."""
    from article.importer import parse_csv, preview_import

    if request.method == "POST":
        upload = request.FILES.get("file")
        if upload is None:
            return render(request, "article/import.html", {"error": "No file uploaded."})
        text = upload.read().decode("utf-8-sig", errors="replace")
        request.session["import_text"] = text
        organisation = active_organisation(request)
        return render(request, "article/importPreview.html", {
            "preview": preview_import(parse_csv(text), organisation),
            "types": ArticleType.objects.filter(organisation=organisation),
            "storages": Storage.objects.filter(organisation=organisation),
        })
    return render(request, "article/import.html", {})


@login_required(login_url='/accounts/login/')
@require_perm("article.create_all")
def importConfirm(request):
    """Apply the preview choices and import (§19)."""
    from article.importer import import_articles, parse_csv

    if request.method != "POST":
        return HttpResponseNotFound('<h1>Page not found</h1>')
    text = request.session.pop("import_text", None)
    if not text:
        return redirect("import articles")
    organisation = active_organisation(request)
    type_choices = {
        name: request.POST.get("type_%s" % name, "skip")
        for name in request.POST.getlist("unknown_type")
    }
    storage_choices = {
        name: request.POST.get("storage_%s" % name, "skip")
        for name in request.POST.getlist("unknown_storage")
    }
    report = import_articles(
        parse_csv(text), organisation, type_choices, storage_choices,
        request.POST.get("duplicates", "skip"),
    )
    return render(request, "article/import.html", {"report": report})


@login_required(login_url='/accounts/login/')
@require_perm("article.create_all")
def importTemplate(request):
    """Downloadable CSV template (§19)."""
    return csv_response(
        "article-import-template.csv",
        ["name", "type", "menge", "storage", "zustand"],
        [["Hammer", "tool", "1", "Regal 1", "gut"]],
    )

