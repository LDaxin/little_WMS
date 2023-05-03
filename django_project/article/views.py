from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from .forms import *
from stored.models import Stored
from django.core.exceptions import ObjectDoesNotExist
from storage.models import Stored
from django.contrib.auth.decorators import login_required


def fListGen(typ):
    fList = []
    notList =["ref"]
    for enableField in ArticleType._meta.get_fields():
        for field in ArticleTemplate._meta.get_fields():
            try:
                if (not field.blank and enableField.name == field.name) or (getattr(typ, enableField.name) and enableField.name == field.name):
                    for notField in notList:
                        if notField != field.name:
                            fList.append(field.name)
            except AttributeError:
                pass
        for field in Article._meta.get_fields():
            try:
                if (not field.blank and enableField.name == field.name) or (getattr(typ, enableField.name) and enableField.name == field.name):
                    for notField in notList:
                        if notField != field.name:
                            fList.append(field.name)
            except AttributeError:
                pass
    return fList


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old
@login_required(login_url='/accounts/login/')
def articles(request, typ):

    t = ArticleType.objects.get(lowerName__exact=typ)

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        fList = fListGen(t)
        return render(request, "article/articles.html", context={"symbol":t.tSymbol, "searchFieldName":"articleSearch" + t.tName, 'type':"article", "name":typ, "form":[FormTemplateArticle , FormArticleBase], "l":fList, "typ":typ})

@login_required(login_url='/accounts/login/')
def addArticle(request, typ):

    t = ArticleType.objects.get(lowerName__exact=typ)
    
    if t == None:
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"no article type named " + typ, "toastType":"alert"})
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
                if t.ref:
                    ref = Stored()
                    ref.save()
                    pa.ref = ref
                    pa.save()
                return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastText":pa.template.name + " was added to your system.", "toastType":"status"})

        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})
    
@login_required(login_url='/accounts/login/')
def delArticle(request, typ):

    t = ArticleType.objects.get(lowerName__exact=typ)
    
    if t == None:
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"no article type named " + typ, "toastType":"alert"})
    else:
        if request.method == "POST":
            delList = []
            delListReturn = ""
            for key, value in request.POST.items():
                if key[0:1] == '_':
                    try:
                        pa = Article.objects.filter(template__pType__tName__exact=typ, pk=value).first()
                        delList.append(pa)
                    except Exception as e:
                        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":e, "toastType":"alert"})
            for i in delList:
                delListReturn = delListReturn + i.__str__() + " "
                i.delete()

            return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastText":delListReturn, "toastType":"alert"})

        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})

@login_required(login_url='/accounts/login/')
def article(request, typ, article_id):

    try:
        p = Article.objects.get(pk=article_id)
        if p.template.pType.tName == typ:
            fList = fListGen(p.template.pType)
            temp = FormTemplateArticle(instance=p.template)
            par = FormArticleBase(instance=p)
            return render(request, "article/modules/article.html", context={"symbol":p.template.pType.tSymbol,"form":[temp , par], "l":fList, "typ":typ})
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.template.pType.tName)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def articleIncert(request, typ, article_id):

    try:
        p = Article.objects.get(pk=article_id)
        if p.template.pType.tName == typ:
            fList = fListGen(p.template.pType)
            temp = FormTemplateArticle(instance=p.template)
            par = FormArticleBase(instance=p)
            return render(request, "article/modules/articleIncert.html", context={"symbol":p.template.pType.tSymbol,"form":[temp, par], "l":fList, "typ":typ})
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + p.template.pType.tName)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')



@login_required(login_url='/accounts/login/')
def tag(request):
    if request.method == "POST":
        t = FormTag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "article/tag.html", context={"list":Tag.objects.all(), "form":[FormTag]})
