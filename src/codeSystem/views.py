from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import csv


# Create your views here.
@login_required(login_url='/accounts/login/')
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


    context = {
        "toastName": "add success",
        "toastId": "successToast",
        "toastText": "added "+ str(request.POST["number"]) + " codes",
        "toastType": "status"
    }
    return render(request, "hub/modules/itemAdd.html", context=context)

@login_required(login_url='/accounts/login/')
def addModal(request):
    context = {
        "modalId":"add",
        "form":[FormCode()],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
def codes(request):
    context = {
        "symbol":"Code",
        "searchFieldName":"codeSearch",
        "name":"code",
        "form":[FormCode()],
        "type":"code",
        "function":["add", "del", "export"]
    }
    return render(request, "hub/modules/items.html", context=context)

@login_required(login_url='/accounts/login/')
def searchCodes(request):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = UuidCode.objects.filter(used=False)
        else:
            r = UuidCode.objects.filter(Q(prefix__contains=request.GET['search']) | Q(code__contains=request.GET['search']))
        return render(request, "hub/modules/results.html", context={"results":r, "type":"code"})

@login_required(login_url='/accounts/login/')
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
