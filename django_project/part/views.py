from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from .forms import *
from django.core.exceptions import ObjectDoesNotExist


def fListGen(typ):
    fList = []
    for enableField in Type._meta.get_fields():
        for field in Template._meta.get_fields():
            try:
                if (not field.null and enableField.name == field.name) or (getattr(typ, enableField.name) and enableField.name == field.name):
                    fList.append(field.name)
            except AttributeError:
                pass
        for field in Part._meta.get_fields():
            try:
                if (not field.null and enableField.name == field.name) or (getattr(typ, enableField.name) and enableField.name == field.name):
                    fList.append(field.name)
            except AttributeError:
                pass
    return fList



def parts(request, typ):

    t = Type.objects.filter(tName__exact=typ).first()

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:

        fList = fListGen(t)

        return render(request, "part/parts.html", context={"symbol":t.tSymbol, 'type':t.tName, "name":"part", "form":[FormTemplatePart , FormPartBase], "l":fList, "typ":True})


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
