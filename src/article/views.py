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
from storage.models import *


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old

@login_required(login_url='/accounts/login/')
def article(request, typ, articleId):
    p = Article.objects.get(pk=articleId)
    if p.base.pType.name == typ:
        bpar = FormArticleBase(instance=p.base, prefix="base")
        par = FormChangeArticle(instance=p, prefix="article")

        par.fields["stored"].initial = p.stored
        context = {
            "symbol":p.base.pType.symbol,
            "searchFieldName":"articleSearch" + p.base.pType.name,
            "id":articleId,
            "modalId":"single",
            "actionType":"update",
            "form":[bpar,par],
            "typ":typ
        }
        return render(request, "hub/modules/item.html", context=context)
    else:
        return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.base.pType.name)

@login_required(login_url='/accounts/login/')
def addModal(request, typ):
    context = {
        "modalId":"add",
        "form":[FormArticleBase(prefix="base"), FormArticle(prefix="article")],
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
            par = FormChangeArticle(instance=p)
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
            "form":[FormArticleBase(prefix="base"), FormArticle(prefix="article")],
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
            pb = FormArticleBase(request.POST, prefix="base")


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

            p = FormArticle(request.POST, prefix="article")
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
                        container = Article.objects.get(code__code=p["stored"].value())
                        if container.space.active == False:
                            context = {
                                "toastName":"Error",
                                "toastId":"errorToast",
                                "toastText":"no active space with code " + p["stored"].value(),
                                "toastType":"alert"
                            }
                            return render(request, "hub/modules/toast.html", context=context)
                        pa.stored = container.space
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
                        storage = Storage.objects.get(code__code=p["stored"].value())
                        pa.stored = storage.space
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
                pa.base = base


                pa.save()

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
            articleBaseForm = FormArticleBase(request.POST, instance=articleObject.base, prefix="base")
            articleForm =  FormArticle(request.POST, instance=articleObject, prefix="article")

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
                try:
                    if articleForm.cleaned_data["stored"].startswith("s0"):
                        space = Storage.objects.get(code__code=str(articleForm.cleaned_data["stored"])).space
                        articleObject.stored = space
                    elif articleForm.cleaned_data["stored"].startswith("a0"):
                        space = Article.objects.get(code__code=str(articleForm.cleaned_data["stored"])).space
                        if space.active == False:
                            context = {
                                "toastName":"Error",
                                "toastId":"errorToast",
                                "toastText":"article code has no space",
                                "toastType":"alert"
                            }
                            return render(request, "hub/modules/toast.html", context=context)
                        articleObject.stored = space
                    elif articleForm.cleaned_data["stored"]=="":
                        pass
                    else:
                        context = {
                            "toastName":"Error",
                            "toastId":"errorToast",
                            "toastText":"no valide code",
                            "toastType":"alert"
                        }
                        return render(request, "hub/modules/toast.html", context=context)

                except:
                    context = {
                        "toastName":"Error",
                        "toastId":"errorToast",
                        "toastText":"no valide code",
                        "toastType":"alert"
                    }
                    return render(request, "hub/modules/toast.html", context=context)

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

    if state == "on":
        context = {
            "input":scannerId,
            "state":state,
            "inputF":scannerId.replace("-", "_"),
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

