from django.shortcuts import render
from .forms import *
from .models import *


# Create your views here.
def warehouse(request):
    if request.method == "POST":
        w = Form_warehouse(request.POST)
        if w.is_valid():
            w.save()
    return render(request, "warehouse/warehouse.html", context={"list": Warehouse.objects.all(),"form":Form_warehouse,  "add":"Lager Hinzufügen"})


def storage(request):
    if request.method == "POST":
        s = Form_storage(request.POST)
        if s.is_valid():
            s.save()
    return render(request, "warehouse/storage.html", context={"list": Storage.objects.all(),"form":Form_storage,  "add":"Lagereinheit Hinzufügen"})
