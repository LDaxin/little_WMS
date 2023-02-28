from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def warehouses(request):
    return render(request, "warehouse/warehouses.html", context={"list": Warehouse.objects.all(), "searchFieldName":"warehouseSearch", "form":[FormWarehouse]})


@login_required(login_url='/accounts/login/')
def addWarehouse(request):
    if request.method == "POST":
        w = FormWarehouse(request.POST)
        if w.is_valid():
            warehouse = w.save(commit=False)
            ref = Stored()
            ref.save()
            warehouse.ref = ref
            war = warehouse.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastText":str(warehouse) + " was added to your system.", "toastType":"status"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})


@login_required(login_url='/accounts/login/')
def storages(request):
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
def shelfs(request):
    return render(request, "warehouse/shelfs.html", context={"list": Shelf.objects.all(), "searchFieldName":"shelfSearch" ,"form":[FormShelf]})

@login_required(login_url='/accounts/login/')
def addShelf(request):
    if request.method == "POST":
        s = FormShelf(request.POST)
        if s.is_valid():
            shelf = s.save(commit=False)
            ref = Stored()
            ref.save()
            shelf.ref = ref
            sh = shelf.save()
            num = 0
            for x in range(1, shelf.rows + 1):
                for y in range(1, shelf.columns + 1):
                    c = Compartment()
                    c.shelf = shelf
                    c.row = x
                    c.colum = y
                    c.name = str(x) + "." + str(y) 
                    ref = Stored()
                    c.ref = ref
                    ref.save()
                    c.save()
                    return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastText":str(shelf) + " was added to your system. with "+ str(num) + "Compartments" , "toastType":"status"})
                    num += 1
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastText":sh + " was added to your system. with "+ str(num) + "Compartments" , "toastType":"status"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})


@login_required(login_url='/accounts/login/')
def compartments(request):
    return render(request, "warehouse/compartments.html", context={"list": Compartment.objects.all()})


@login_required(login_url='/accounts/login/')
def addCompartment(request):
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})
