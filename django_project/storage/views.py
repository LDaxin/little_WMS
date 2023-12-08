from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required(login_url='/accounts/login/')
def storage(request, typ, storageId):
        storageObject = Storage.objects.get(pk=storageId)

        if storageObject.typ.lowerName == typ:
            instancedStorageForum = FormChangeStorage(instance=storageObject)
            context = {
                "symbol":storageObject.typ.symbol,
                "searchFieldName":"storageSearch" + storageObject.typ.name,
                "modalId":"single",
                "form":[instancedStorageForum],
                "typ":typ,
                "actionType":"update",
                "id":storageId
            }
            return render(request, "hub/modules/item.html", context=context)
        else:
            return HttpResponseNotFound('<h1>wrong type</h1>' + typ + storageObject.typ.name)
    

@login_required(login_url='/accounts/login/')
def storageIncert(request, typ, storageId):
    try:
        storageObject = Storage.objects.get(pk=storageId)
        if storageObject.typ.lowerName == typ:
            instancedStorageForum = FormChangeStorage(instance=storageObject)
            context = {
                "symbol":storageObject.typ.symbol,
                "searchFieldName":"storageSearch" + storageObject.typ.name,
                "modalId":"single",
                "form":[instancedStorageForum],
                "typ":typ,
                "actionType":"update",
                "id":storageId
            }
            return render(request, "hub/modules/itemForm.html", context=context)
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
        context = {
            "symbol":storageTypeObject.symbol,
            "searchFieldName":"storageSearch" + storageTypeObject.name,
            'type':"storage",
            "name":typ,
            "form":[FormStorage()],
            "typ":typ
        }
        return render(request, "hub/modules/items.html", context=context)

@login_required(login_url='/accounts/login/')
def addModal(request, typ):
    context = {
        "modalId":"add",
        "form":[FormStorage()],
        "actionType":"add",
    }
    return render(request, "hub/modules/addForm.html", context=context)

@login_required(login_url='/accounts/login/')
def delModal(request, typ):
    context = {
        "modalId":"del",
        "form":[FormStorage()],
        "actionType":"del",
    }
    return render(request, "hub/modules/delForm.html", context=context)

@login_required(login_url='/accounts/login/')
def addStorage(request, typ):

    t = StorageType.objects.get(lowerName__exact=typ)

    if request.method == "POST":
        s = FormStorage(request.POST)
        if s.is_valid():
            storage = s.save(commit=False)
            storage.typ = t
            so = storage.save()
            context = {
                "toastName":"Add Succses",
                "toastId":"successToast",
                "toastText":str(storage) + " was added to your system.",
                "toastType":"status"
            }
            return render(request, "hub/modules/itemAdd.html", context=context)
        context = {
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)
    context = {
        "toastName":"Error",
        "toastId":"errorToast",
        "toastText":"something went wrong",
        "toastType":"alert"
    }
    return render(request, "hub/modules/toast.html", context=context)

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
                    context = {
                        "toastName":"Error",
                        "toastId":"errorToast",
                        "toastText":e,
                        "toastType":"alert"
                    }
                    return render(request, "hub/modules/toast.html", context=context)
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()

        context = {
            "toastName":"Delete",
            "toastId":"successToast",
            "toastText":delListReturn,
            "toastType":"status"
        }
        return render(request, "hub/modules/itemDelete.html", context=context)
    context = {
        "toastName":"Error",
        "toastId":"errorToast",
        "toastText":"something went wrong",
        "toastType":"alert"
    }
    return render(request, "hub/modules/toast.html", context=context)

@login_required(login_url='/accounts/login/')
def updateStorage(request, storageId, typ):
    storageObject = Storage.objects.get(pk=storageId)

    if request.method == "POST":
        form = FormStorage(request.POST, instance=storageObject)
        if form.is_valid():
            form.save()
            context = {
                "toastName":"Update",
                "toastId":"successToast",
                "toastText":str(storageObject) + " was updated",
                "toastType":"status"
            }
            return render(request, "hub/modules/toast.html", context=context)
        context ={
            "toastName":"Error",
            "toastId":"errorToast",
            "toastText":"something went wrong",
            "toastType":"alert"
        }
        return render(request, "hub/modules/toast.html", context=context)


@login_required(login_url='/accounts/login/')
def searchStorages(request, typ):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = Storage.objects.filter(typ__lowerName__exact=typ)
        else:
            r = Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), typ__lowerName__exact=typ)
        return render(request, "hub/modules/results.html", context={"results":r, "type":"storage"})
