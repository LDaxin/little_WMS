from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
        "toastName": "Error",
        "toastId": "errorToast",
        "toastText": "something went wrong",
        "toastType": "alert"
    }
    return render(request, "hub/modules/toast.html", context=context)


@login_required(login_url='/accounts/login/')
def codes(request):
    context = {
        "symbol":"Code",
        "searchFieldName":"codeSearch",
        "name":"code",
        "form":[FormCode()],
        "type":"code"
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

