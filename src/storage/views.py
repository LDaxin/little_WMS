from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from codeSystem.models import *
from article.models import Article, Stock
from article.views import composition_context, composition_warning
from tag.models import Tag
from movement.services import MovementService
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from django.core.exceptions import ValidationError
from django.db.models import Q
import csv
from time import sleep

@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storage(request, typ, storageId):
        storageObject = Storage.objects.get(pk=storageId)

        if storageObject.typ.name == typ:
            instancedStorageForum = FormChangeStorage(instance=storageObject)
            context = {
                "symbol":storageObject.typ.symbol,
                "searchFieldName":"storageSearch" + storageObject.typ.name,
                "modalId":"single",
                "form":[instancedStorageForum],
                "typ":typ,
                "actionType":"update",
                "id":storageId,
                "code":storageObject.code.code if storageObject.code else "",
                "link":("/s/" + storageObject.code.code) if storageObject.code else "",
                "storageContents":True,
                "contents":Stock.objects.filter(stored=storageObject.space),
                "storeUrl":"./%s/store" % storageId,
                "removeUrl":"./%s/remove" % storageId,
                "tagChips":True,
                "tags":storageObject.tags.all(),
                "allTags":Tag.objects.all(),
                "tagAddUrl":"./%s/tags/add" % storageId,
                "tagRemoveUrl":"./%s/tags/remove" % storageId,
            }
            context.update(composition_context(storageObject.space))
            return render(request, "hub/modules/item.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)
    

@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def storageIncert(request, typ, storageId):
    try:
        storageObject = Storage.objects.get(pk=storageId)
        if storageObject.typ.name == typ:
            instancedStorageForum = FormChangeStorage(instance=storageObject)
            context = {
                "symbol":storageObject.typ.symbol,
                "searchFieldName":"storageSearch" + storageObject.typ.name,
                "modalId":"single",
                "form":[instancedStorageForum],
                "typ":typ,
                "actionType":"update",
                "id":storageId
            }
            return render(request, "hub/modules/itemForm.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storages(request, typ):

    storageTypeObject = StorageType.objects.get(name__exact=typ)

    if storageTypeObject == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        context = {
            "symbol":storageTypeObject.symbol,
            "searchFieldName":"storageSearch" + storageTypeObject.name,
            'type':"storage",
            "name":typ,
            "form":[FormStorage()],
            "typ":typ,
            "add":True,
            "del":True,
            "export":True,
            "qr":True
        }
        return render(request, "hub/modules/items.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("storage.create_all")
def addModal(request, typ):
    context = {
        "modalId":"add",
        "form":[FormStorage()],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("storage.delete_all")
def delModal(request, typ):
    context = {
        "modalId":"del",
        "form":[FormStorage()],
        "actionType":"del",
    }
    return render(request, "hub/modules/delForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("storage.create_all")
def addStorage(request, typ):

    t = StorageType.objects.get(name__exact=typ)

    if request.method == "POST":
        s = FormStorage(request.POST)
        if s.is_valid():
            storage = s.save(commit=False)
            storage.typ = t
            if s["code"].value().startswith("s0"):
                try:
                    code = UuidCode.objects.get(code=s["code"].value())
                    if code.used:
                        context = {
                            "toastName":"Error",
                            "toastId":"errorToast",
                            "toastText":"code is already used",
                            "toastType":"alert"
                        }
                        return render(request, "hub/modules/toast.html", context=context)
                    code.used = True
                    code.save()
                    storage.code = code
                except:
                    context = {
                        "toastName":"Error",
                        "toastId":"errorToast",
                        "toastText":"not valid code",
                        "toastType":"alert"
                    }
                    return render(request, "hub/modules/toast.html", context=context)
            else:
                pass

            so = storage.save()
            context = {
                "toastName":"Add Succses",
                "toastId":"successToast",
                "toastText":str(storage) + " was added to your system.",
                "toastType":"status"
            }
            return render(request, "hub/modules/itemAdd.html", context=context)
        context = {
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)
    context = {
        "toastName":"Error",
        "toastId":"errorToast",
        "toastText":"something went wrong",
        "toastType":"alert"
    }
    return render(request, "hub/modules/toast.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("storage.delete_all")
def delStorage(request, typ):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        childList = []
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Storage.objects.filter(pk=value).first()
                    ch = Storage.objects.filter(parent__pk=value)
                    delListReturn = delListReturn + pa.__str__() + ", "
                    for i in ch:
                        i.parent = None
                        i.save()
                    pa.delete()
                except Exception as e:
                    context = {
                        "toastName":"Error",
                        "toastId":"errorToast",
                        "toastText":e,
                        "toastType":"alert"
                    }
                    return render(request, "hub/modules/toast.html", context=context)

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
@require_perm("storage.edit_all")
def updateStorage(request, storageId, typ):
    storageObject = Storage.objects.get(pk=storageId)

    if request.method == "POST":
        form = FormStorage(request.POST, instance=storageObject)
        if form.is_valid():
            form.save()
            context = {
                "toastName":"Update",
                "toastId":"successToast",
                "toastText":str(storageObject) + " was updated",
                "toastType":"status"
            }
            return render(request, "hub/modules/toast.html", context=context)
        context ={
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)


def _storage_contents_context(storage, storeUrl, removeUrl, error="", warning="", forceCode=""):
    return {
        "contents": Stock.objects.filter(stored=storage.space).select_related("article__base"),
        "storeUrl": storeUrl,
        "removeUrl": removeUrl,
        "storeSearchUrl": storeUrl + "-search",
        "storeError": error,
        "storeWarning": warning,
        "forceCode": forceCode,
    }


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def storeInStorage(request, typ, storageId):
    storage = Storage.objects.get(pk=storageId)
    storeUrl = "./%s/store" % storageId
    removeUrl = "./%s/remove" % storageId
    if request.method == "POST":
        code = request.POST.get("code", "")
        try:
            article = Article.objects.get(code__code=code)
            warning = composition_warning(storage.space, article)
            if warning and not request.POST.get("force"):
                return render(request, "hub/modules/storageContents.html",
                              context=_storage_contents_context(storage, storeUrl, removeUrl,
                                                                warning=warning, forceCode=code))
            amount = request.POST.get("amount", "").strip()
            amount = int(amount) if amount.isdigit() else None
            MovementService.store_article(article, storage.space, request.user, amount=amount)
            error = ""
        except Article.DoesNotExist:
            error = "No article with that code"
        except ValidationError as e:
            error = e.messages[0] if e.messages else str(e)
        return render(request, "hub/modules/storageContents.html",
                      context=_storage_contents_context(storage, storeUrl, removeUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def storeArticleSearch(request, typ, storageId):
    """Live suggestions for the store-article field (code or name, § code-input)."""
    query = request.GET.get("code", "").strip()
    if query:
        articles = Article.objects.filter(
            Q(base__name__contains=query) | Q(code__code__contains=query)
        )[:20]
    else:
        articles = Article.objects.none()
    return render(request, "hub/modules/storeArticleResults.html", {
        "articles": articles,
        "storeUrl": "./%s/store" % storageId,
    })


@login_required(login_url='/accounts/login/')
@require_perm("article.move_all")
def removeFromStorage(request, typ, storageId, articleId):
    storage = Storage.objects.get(pk=storageId)
    storeUrl = "./%s/store" % storageId
    removeUrl = "./%s/remove" % storageId
    if request.method == "POST":
        article = Article.objects.get(pk=articleId)
        MovementService.remove_article(article, space=storage.space, user=request.user)
        return render(request, "hub/modules/storageContents.html",
                      context=_storage_contents_context(storage, storeUrl, removeUrl))
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
@require_perm("storage.edit_all")
def addStorageTag(request, typ, storageId):
    storage = Storage.objects.get(pk=storageId)
    tagAddUrl = "./%s/tags/add" % storageId
    tagRemoveUrl = "./%s/tags/remove" % storageId
    if request.method == "POST":
        name = request.POST.get("tag", "").strip()
        tag = Tag.objects.filter(name__iexact=name).first()
        if tag is None:
            error = "No tag named %s" % name
        else:
            storage.tags.add(tag)
            error = ""
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(storage, tagAddUrl, tagRemoveUrl, error))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("storage.edit_all")
def removeStorageTag(request, typ, storageId, tagId):
    storage = Storage.objects.get(pk=storageId)
    tagAddUrl = "./%s/tags/add" % storageId
    tagRemoveUrl = "./%s/tags/remove" % storageId
    if request.method == "POST":
        storage.tags.remove(Tag.objects.get(pk=tagId))
        return render(request, "hub/modules/tagChips.html",
                      context=_tag_chips_context(storage, tagAddUrl, tagRemoveUrl))
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def searchStorages(request, typ):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = Storage.objects.filter(typ__name__exact=typ)
        else:
            r = Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), typ__name__exact=typ)
        return render(request, "hub/modules/results.html", context={"results":r, "type":"storage"})


@login_required(login_url='/accounts/login/')
@require_perm("export.csv_all")
def exportStorages(request, typ):
    response = HttpResponse(content_type='text/csv; charset=iso-8859-1')
    response['Content-Disposition'] = 'attachment; filename="storages.csv"'

    thereIsOne = False

    writer = csv.writer(response, dialect="excel")
    writer.writerow(['name', 'code', 'type'])
    for key, value in request.POST.items():
        if key.startswith("_"):
            storage = Storage.objects.get(pk=value)
            if storage.typ.name == typ:
                thereIsOne = True
                writer.writerow([storage.name, storage.code.code, storage.typ.name])
    return response

@login_required(login_url='/accounts/login/')
@require_perm("storage.view_all")
def storageScanner(request, typ, scannerId, state):
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
