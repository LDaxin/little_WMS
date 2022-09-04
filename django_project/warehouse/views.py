from django.shortcuts import render
from .forms import *
from .models import *

# Create your views here.
def warehouse(request):
    return render(request, "warehouse/warehouse.html", context={"list": Warehouse.objects.all(),"form":Form_warehouse,  "add":"Lager Hinzufügen"})

    