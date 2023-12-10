from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from codeSystem.models import *
from .forms import *
from space.models import Space
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import csv


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old

@login_required(login_url='/accounts/login/')
def article(request, typ, articleId):
    p = Article.objects.get(pk=articleId)
    if p.pType.name == typ:
        par = FormChangeArticle(instance=p)
        context = {
            "symbol":p.pType.symbol,
            "searchFieldName":"articleSearch" + p.pType.name,
            "id":articleId,
            "modalId":"single",
            "form":[par],
            "actionType":"update",
            "typ":typ
        }
        return render(request, "hub/modules/item.html", context=context)
    else:
        return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.pType.name)

@login_required(login_url='/accounts/login/')
def addModal(request, typ):
    context = {
        "modalId":"add",
        "form":[FormArticle()],
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
        if p.pType.name == typ:
            par = FormChangeArticle(instance=p)
            context = {
                "symbol":p.pType.symbol,
                "searchFieldName":"articleSearch" + p.pType.name,
                "id":articleId,
                "modalId":"single",
                "form":[par],
                "actionType":"update",
                "typ":typ,
            }
            return render(request, "hub/modules/itemForm.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.pType.name)
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
            "form":[FormArticle()],
            "typ":typ
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
            p = FormArticle(request.POST)
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


                if p["stored"].value().startswith("a0"):
                    try:
                        space = Artice.objects.get(code__code=int(p["stored"].value()))
                        if space.space.active == False:
                            context = {
                                "toastName":"Error",
                                "toastId":"errorToast",
                                "toastText":"no active space with code " + p["stored"].value(),
                                "toastType":"alert"
                            }
                            return render(request, "hub/modules/toast.html", context=context)
                        pa.space = space

                    except:
                        context = {
                            "toastName":"Error",
                            "toastId":"errorToast",
                            "toastText":"no article with code " + p["stored"].value(),
                            "toastType":"alert"
                        }
                        return render(request, "hub/modules/toast.html", context=context)
                elif p["stored"].value().startswith("s0"):
                    try:
                        space = Space.objects.get(code__code=int(p["stored"].value()))
                        pa.space = space
                    except:
                        context = {
                            "toastName":"Error",
                            "toastId":"errorToast",
                            "toastText":"no space with code " + p["stored"].value(),
                            "toastType":"alert"
                        }
                        return render(request, "hub/modules/toast.html", context=context)
                elif p["stored"].value() == "":
                    pass
                else:
                    context = {
                        "toastName":"Error",
                        "toastId":"errorToast",
                        "toastText":"code" + p["stored"].value() + " not found",
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
                "toastText":"no article type named " + typ + str(request.POST["stored"]),
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
                        pa = Article.objects.filter(pType__name__exact=typ, pk=value).first()
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
            r = Article.objects.filter(pType__name__exact=typ)
        else:
            r = Article.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), pType__name__exact=typ)
        return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})

@login_required(login_url='/accounts/login/')
def exportArticles(request, typ):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="articles.csv"'

    thereIsOne = False

    writer = csv.writer(response)
    writer.writerow(['name', 'code', 'type'])
    for key, value in request.POST.items():
        if key.startswith("_"):
            article = Article.objects.get(pk=value)
            if article.pType.name == typ:
                thereIsOne = True
                writer.writerow([article.name, article.code.code, article.pType.name])
    return response

@login_required(login_url='/accounts/login/')
def articleScanner(request, typ, scannerId, state):
    if state == "on":
        context = {
            "input":scannerId,
            "state":state
        }
        return render(request, "hub/modules/toggleScanner.html", context=context)

    elif state == "off":
        context = {
            "input":scannerId,
            "state":state
        }
        return render(request, "hub/modules/toggleScanner.html", context=context)

    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

