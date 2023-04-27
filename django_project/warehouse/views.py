from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def storage(request):
    return render(request, "warehouse/storages.html", context={"list": Storage.objects.all(), "searchFieldName":"storageSearch" , "form":[FormStorage]})

@login_required(login_url='/accounts/login/')
def storages(request, typ):
    return render(request, "warehouse/storages.html", context={"list": Storage.objects.all(), "searchFieldName":"storageSearch" , "form":[FormStorage]})

@login_required(login_url='/accounts/login/')
def addStorage(request):
    if request.method == "POST":
        s = FormStorage(request.POST)
        if s.is_valid():
            storage = s.save(commit=False)
            ref = Stored()
            ref.save()
            storage.ref = ref
            so = storage.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastText":str(storage) + " was added to your system.", "toastType":"status"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})

@login_required(login_url='/accounts/login/')
def delStorage(request):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Storage.objects.filter(pk=value).first()
                    delList.append(pa)
                except Exception as e:
                    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":e, "toastType":"alert"})
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()

        return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastText":delListReturn, "toastType":"alert"})

    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})

