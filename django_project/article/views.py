from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from .forms import *
from space.models import Space
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old

@login_required(login_url='/accounts/login/')
def article(request, typ, articleId):
    p = Article.objects.get(pk=articleId)
    if p.pType.lowerName == typ:
        par = FormChangeArticle(instance=p)
        context = {
            "symbol":p.pType.tSymbol,
            "searchFieldName":"articleSearch" + p.pType.tName,
            "id":articleId,
            "modalId":"single",
            "form":[par],
            "actionType":"update",
            "typ":typ
        }
        return render(request, "hub/modules/item.html", context=context)
    else:
        return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.pType.tName)

@login_required(login_url='/accounts/login/')
def addModal(request, typ):
    context = {
        "modalId":"add",
        "form":[FormArticle()],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
def articleIncert(request, typ, articleId):
    try:
        p = Article.objects.get(pk=articleId)
        if p.pType.lowerName == typ:
            par = FormChangeArticle(instance=p)
            context = {
                "symbol":p.pType.tSymbol,
                "searchFieldName":"articleSearch" + p.pType.tName,
                "id":articleId,
                "modalId":"single",
                "form":[par],
                "actionType":"update",
                "typ":typ,
            }
            return render(request, "hub/modules/itemForm.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.pType.tName)
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def articles(request, typ):
    t = ArticleType.objects.get(lowerName__exact=typ)

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        context={
            "symbol":t.tSymbol,
            "searchFieldName":"articleSearch" + t.tName,
            'type':"article",
            "name":typ,
            "form":[FormArticle()],
            "typ":typ
        }
        return render(request, "hub/modules/items.html", context=context)

@login_required(login_url='/accounts/login/')
def addArticle(request, typ):
    t = ArticleType.objects.get(lowerName__exact=typ)
    
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
            p = FormArticle(request.POST)
            if p.is_valid():

                pa = p.save(commit=False)
                pa.pType = t
                space = Space()
                if t.article_toggle_space:
                    space.active = True
                else:
                    space.active = False
                space.prefix = "a0"
                space.save()
                pa.space = space

                pa.save()

                context = {
                    "toastName":"Add Succses",
                    "toastId":"successToast",
                    "toastText":pa.name + " was added to your system.",
                    "toastType":"status"
                }

                return render(request, "hub/modules/itemAdd.html", context=context)

        context = {
                "toastName":"Error",
                "toastId":"errorToast",
                "toastText":"no article type named " + typ,
                "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)

@login_required(login_url='/accounts/login/')
def delArticle(request, typ):
    t = ArticleType.objects.get(lowerName__exact=typ)
    
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
                        pa = Article.objects.filter(pType__lowerName__exact=typ, pk=value).first()
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
            return render(request, "hub/modules/toast.html", context=context)

        context = {
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)

@login_required(login_url='/accounts/login/')
def updateArticle(request, typ, articleId):
    articleTypeObject = ArticleType.objects.get(lowerName__exact=typ)
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
            articleForm = FormArticle(request.POST, instance=articleObject)
            if articleForm.is_valid():
                articleForm.save()
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

@login_required(login_url='/accounts/login/')
def searchArticle(request, typ):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = Article.objects.filter(pType__lowerName__exact=typ)
        else:
            r = Article.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), pType__lowerName__exact=typ)
        return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})
