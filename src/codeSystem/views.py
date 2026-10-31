from django.utils.translation import gettext as _
from hub.toasts import toast
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from organisation.decorators import require_perm
from django.db.models import Q
import csv


# Create your views here.
@login_required(login_url='/accounts/login/')
@require_perm("code.create_all")
def addCode(request):
    if request.method == "POST":
        form = FormCode(request.POST)
        if form.is_valid():
            for number in range(0, int(request.POST["number"])):
                code = UuidCode()
                if request.POST["types"] == "1":
                    code.prefix = "a0"
                    code.used = False
                    code.save()
                elif request.POST["types"] == "2":
                    code.prefix = "s0"
                    code.used = False
                    code.save()
                else:
                    pass


    return toast(request, _("add success"), _("added ")+ str(request.POST["number"]) + " codes", "status", template="hub/modules/itemAdd.html")

@login_required(login_url='/accounts/login/')
@require_perm("code.view_all")
def addModal(request):
    context = {
        "modalId":"add",
        "form":[FormCode()],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("code.view_all")
def codes(request):
    context = {
        "symbol":"Code",
        "searchFieldName":"codeSearch",
        "name":"code",
        "form":[FormCode()],
        "type":"code",
        "add":True,
        "del":False,
        "export":True
    }
    return render(request, "hub/modules/items.html", context=context)

@login_required(login_url='/accounts/login/')
@require_perm("code.view_all")
def searchCodes(request):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = UuidCode.objects.filter(used=False)
        else:
            r = UuidCode.objects.filter(Q(prefix__contains=request.GET['search']) | Q(code__contains=request.GET['search']))
        return render(request, "hub/modules/results.html", context={"results":r, "type":"code"})

@login_required(login_url='/accounts/login/')
@require_perm("code.view_all")
def resolve_code(request, kind, code):
    """Canonical link by code (§26): /a/<code>, /s/<code>, /l/<code>."""
    from article.models import Article
    from storage.models import Storage
    from location.models import Location

    if kind == "a":
        article = Article.objects.filter(code__code=code).first()
        if article:
            return redirect("/article/%s/%s" % (article.base.pType.name, article.pk))
    elif kind == "s":
        storage = Storage.objects.filter(code__code=code).first()
        if storage:
            return redirect("/storage/%s/%s" % (storage.typ.name, storage.pk))
    elif kind == "l":
        location = Location.objects.filter(code__code=code).first()
        if location:
            return redirect("/location/%s" % location.pk)
    raise Http404("no object with code %s" % code)


@login_required(login_url='/accounts/login/')
@require_perm("code.export_all")
def codesExport(request):
    response = HttpResponse(content_type='text/csv; charset=iso-8859-1')
    response['Content-Disposition'] = 'attachment; filename="codes.csv"'

    thereIsOne = False

    writer = csv.writer(response, dialect="excel")
    writer.writerow(['prefix', 'code', 'type'])
    for key, value in request.POST.items():
        if key.startswith("_"):
            code = UuidCode.objects.get(pk=value)
            if code.used == False:
                if code.prefix == "a0":
                    typ = "Material/Behälter"
                elif code.prefix == "s0":
                    typ = "Lager"
                else:
                    typ = "unknown"
                thereIsOne = True
                writer.writerow([code.prefix, code.code, typ])
    return response
