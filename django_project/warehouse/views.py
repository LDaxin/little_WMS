from django.shortcuts import render
from .forms import *
from .models import *


# Create your views here.
def warehouses(request):
    if request.method == "POST":
        w = FormWarehouse(request.POST)
        if w.is_valid():
            warehouse = w.save(commit=False)
            ref = Stored()
            ref.save()
            warehouse.ref = ref
            warehouse.save()
    return render(request, "warehouse/warehouses.html", context={"list": Warehouse.objects.all(),"form":[FormWarehouse]})


def storages(request):
    if request.method == "POST":
        s = FormStorage(request.POST)
        if s.is_valid():
            storage = s.save(commit=False)
            ref = Stored()
            ref.save()
            storage.ref = ref
            storage.save()
    return render(request, "warehouse/storages.html", context={"list": Storage.objects.all(), "form":[FormStorage]})


def shelfs(request):
    if request.method == "POST":
        s = FormShelf(request.POST)
        if s.is_valid():
            shelf = s.save(commit=False)
            ref = Stored()
            ref.save()
            shelf.ref = ref
            shelf.save()
            for x in range(1, shelf.rows + 1):
                for y in range(1, shelf.columns + 1):
                    c = Compartment()
                    c.shelf = shelf
                    c.row = x
                    c.colum = y
                    ref = Stored()
                    c.ref = ref
                    ref.save()
                    c.save()
    return render(request, "warehouse/shelfs.html", context={"list": Shelf.objects.all(),"form":[FormShelf]})


def compartments(request):
    return render(request, "warehouse/compartments.html", context={"list": Compartment.objects.all()})
