from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *


# Create your views here.
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


def codes(request):
    context = {
        "symbol":"Code",
        "searchFieldName":"codeSearch",
        "name":"code",
        "form":[FormCode()],
        "type":"code"
    }
    return render(request, "hub/modules/items.html", context=context)

