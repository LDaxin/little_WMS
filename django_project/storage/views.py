from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def storage(request, typ, storageId):
    try:
        storageObject = Storage.objects.get(pk=storageId)

        if storageObject.typ.lowerName == typ:
            instancedStorageForum = FormStorage(instance=storageObject, typ=storageObject.typ)
            return render(request, "hub/modules/item.html", context={"symbol":storageObject.typ.symbol,"form":[instancedStorageForum],  "typ":typ, "actionType":"update"})
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def storageIncert(request, typ, storageId):
    try:
        storageObject = Storage.objects.get(pk=storageId)
        if storageObject.typ.lowerName == typ:
            instancedStorageForum = FormStorage(instance=storageObject, typ=storageObject.typ)
            return render(request, "hub/modules/itemForm.html", context={"symbol":storageObject.typ.symbol,"form":[instancedStorageForum],  "typ":typ, "actionType":"update"})
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)
    
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required(login_url='/accounts/login/')
def storages(request, typ):

    storageTypeObject = StorageType.objects.get(lowerName__exact=typ)

    if storageTypeObject == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return render(request, "hub/modules/items.html", context={"symbol":storageTypeObject.symbol, "searchFieldName":"storageSearch" + storageTypeObject.name, 'type':"storage", "name":typ, "form":[FormStorage(typ=storageTypeObject)],  "typ":typ})

@login_required(login_url='/accounts/login/')
def addStorage(request, typ):

    t = StorageType.objects.get(lowerName__exact=typ)

    if request.method == "POST":
        s = FormStorage(request.POST)
        if s.is_valid():
            storage = s.save(commit=False)
            storage.typ = t
            so = storage.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastId":"successToast", "toastText":str(storage) + " was added to your system.", "toastType":"status"})
        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})

@login_required(login_url='/accounts/login/')
def delStorage(request, typ):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Storage.objects.filter(pk=value).first()
                    delList.append(pa)
                except Exception as e:
                    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":e, "toastType":"alert"})
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()

        return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastId":"successToast", "toastText":delListReturn, "toastType":"alert"})

    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})

