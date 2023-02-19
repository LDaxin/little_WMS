from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from warehouse.models import Stored


def fListGen(typ):
    fList = []
    notList =["ref"]
    for enableField in Type._meta.get_fields():
        for field in Template._meta.get_fields():
            try:
                if (not field.blank and enableField.name == field.name) or (getattr(typ, enableField.name) and enableField.name == field.name):
                    for notField in notList:
                        if notField != field.name:
                            fList.append(field.name)
            except AttributeError:
                pass
        for field in Part._meta.get_fields():
            try:
                if (not field.blank and enableField.name == field.name) or (getattr(typ, enableField.name) and enableField.name == field.name):
                    for notField in notList:
                        if notField != field.name:
                            fList.append(field.name)
            except AttributeError:
                pass
    return fList


# TODO make that if a new template gets created were there is a similar or equal one that there is a question if you want to create a new one or build from the old
def parts(request, typ):

    t = Type.objects.get(tName__exact=typ)

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        if request.method == "POST":
            re = request.POST.copy()
            re["pType"] = str(t.id) 
            te = FormTemplatePart(re)
            if te.is_valid():
                template = te.save()
                re["template"] = template 
                p = FormPartBase(re)
                if t.ref:
                    ref = Stored()
                    ref.save()
                    p.ref = ref
                if p.is_valid():
                    p.save()


        fList = fListGen(t)

        return render(request, "part/parts.html", context={"symbol":t.tSymbol, "searchFieldName":"partSearch" + t.tName, 'type':"part", "name":typ, "form":[FormTemplatePart , FormPartBase], "l":fList, "typ":typ})


def part(request, typ, part_id):

    try:

        p = Part.objects.get(pk=part_id)

        if typ != p.template.pType.tName:

            return HttpResponseNotFound('<h1>Page not found 404</h1>')

        fList = fListGen(p)

        return render(request, "part/part.html", context={"symbol":p.template.pType,"form":[FormTemplatePart , FormPartBase], "l":fList})

    except ObjectDoesNotExist:

        return HttpResponseNotFound('<h1>Page not found 404</h1>')


def tag(request):
    if request.method == "POST":
        t = FormTag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "part/tag.html", context={"list":Tag.objects.all(), "form":[FormTag]})
