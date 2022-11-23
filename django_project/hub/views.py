from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def hub(request):
    return render(request, "hub/hub.html", context={"symbol":"Logo", "fields":['Check_in', 'Check_out', 'Part', 'Container', 'Shelf', 'Storage', 'Warehouse', 'Location', 'Search']})

def manage(request):
    return render(request, "hub/manage.html")

def locations(request):
    if request.method == "POST":
        l = Form_location(request.POST)
        if l.is_valid():
            location = l.save()
            location.save()
    else:
        form =Form_location()
    return render(request, "hub/location.html", context={"list":Location.objects.all(), "form":[[Form_location]]})

