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
def articles(request, typ):

    t = ArticleType.objects.get(lowerName__exact=typ)

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return render(request, "hub/modules/items.html", context={"symbol":t.tSymbol, "searchFieldName":"articleSearch" + t.tName, 'type':"article", "name":typ, "form":[FormTemplateArticle(typ=t), FormArticleBase(typ=t)],  "typ":typ})

@login_required(login_url='/accounts/login/')
def addArticle(request, typ):

    t = ArticleType.objects.get(lowerName__exact=typ)
    
    if t == None:
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"no article type named " + typ, "toastType":"alert"})
    else:
        if request.method == "POST":
            re = request.POST.copy()
            re["pType"] = str(t.id) 
            te = FormTemplateArticle(re)
            if te.is_valid():
                template = te.save()
                re["template"] = template 
                p = FormArticleBase(re)
                if p.is_valid():
                    pa = p.save()
                if t.article_toggle_ref:
                    ref = Stored()
                    ref.save()
                    pa.ref = ref
                    pa.save()
                return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastId":"successToast", "toastText":pa.template.name + " was added to your system.", "toastType":"status"})

        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})
    
@login_required(login_url='/accounts/login/')
def delArticle(request, typ):

    t = ArticleType.objects.get(lowerName__exact=typ)
    
    if t == None:
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"no article type named " + typ, "toastType":"alert"})
    else:
        if request.method == "POST":
            delList = []
            delListReturn = ""
            for key, value in request.POST.items():
                if key.startswith("_"):
                    try:
                        pa = Article.objects.filter(template__pType__lowerName__exact=typ, pk=value).first()
                        delList.append(pa)
                    except Exception as e:
                        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":e, "toastType":"alert"})
            for i in delList:
                delListReturn = delListReturn + i.__str__() + " "
                i.delete()

            return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastId":"successToast", "toastText":delListReturn, "toastType":"alert"})

        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})

@login_required(login_url='/accounts/login/')
def article(request, typ, articleId):

    try:
        p = Article.objects.get(pk=articleId)
        if p.template.pType.lowerName == typ:
            temp = FormTemplateArticle(instance=p.template, typ=p.template.pType)
            par = FormArticleBase(instance=p, typ=p.template.pType)
            return render(request, "hub/modules/item.html", context={"symbol":p.template.pType.tSymbol,"form":[temp , par],  "typ":typ, "actionType":"update"})
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.template.pType.tName)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def articleIncert(request, typ, articleId):

    try:
        p = Article.objects.get(pk=articleId)
        if p.template.pType.lowerName == typ:
            temp = FormTemplateArticle(instance=p.template, typ=p.template.pType)
            par = FormArticleBase(instance=p, typ=p.template.pType)
            return render(request, "hub/modules/itemForm.html", context={"symbol":p.template.pType.tSymbol,"form":[temp, par],  "typ":typ, "actionType":"update"})
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.template.pType.tName)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def articleChange(request, typ, articleId):

    t = ArticleType.objects.get(lowerName__exact=typ)
    
    if t == None:
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"toastError", "toastText":"no article type named " + typ, "toastType":"alert"})
    else:
        if request.method == "POST":
            pass

def articleTemplateChange(request, typ, articleId):

    t = ArticleType.objects.get(lowerName__exact=typ)
    
    if t == None:
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"toastError", "toastText":"no article type named " + typ, "toastType":"alert"})
    else:
        if request.method == "POST":
            pass

@login_required(login_url='/accounts/login/')
def tag(request):
    if request.method == "POST":
        t = FormTag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "article/tag.html", context={"list":Tag.objects.all(), "form":[FormTag]})
