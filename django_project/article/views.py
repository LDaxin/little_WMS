from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from .forms import *
from stored.models import Stored
from django.core.exceptions import ObjectDoesNotExist
from storage.models import Stored
from django.contrib.auth.decorators import login_required


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old

@login_required(login_url='/accounts/login/')
def article(request, typ, articleId):
    try:
        p = Article.objects.get(pk=articleId)
        if p.pType.lowerName == typ:
            par = FormArticleBase(instance=p)
            context = {
                "symbol":p.pType.tSymbol,
                "searchFieldName":"articleSearch" + p.pType.tName,
                "id":articleId,
                "modalId":"single",
                "form":[par],
                "typ":typ
            }
            return render(request, "hub/modules/item.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.pType.tName)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def articleIncert(request, typ, articleId):
        p = Article.objects.get(pk=articleId)
        if p.pType.lowerName == typ:
            par = FormArticleBase(instance=p)
            context = {
                "symbol":p.pType.tSymbol,
                "searchFieldName":"articleSearch" + p.pType.tName,
                "id":articleId,
                "modalId":"single",
                "form":[par],
                "typ":typ
            }
            return render(request, "hub/modules/itemForm.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.pType.tName)

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

                if t.article_toggle_ref:
                    ref = Stored()
                    ref.save()
                    pa.ref = ref

                pa.save()

                context = {
                    "toastName":"Add Succses",
                    "toastId":"successToast",
                    "toastText":pa.name + " was added to your system.",
                    "toastType":"status"
                }

                return render(request, "hub/modules/toast.html", context=context)

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
            articleBaseForm = FormArticleBase(request.POST, instance=articleObject)
            if articleBaseForm.is_valid():
                articleBaseForm.save()
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

