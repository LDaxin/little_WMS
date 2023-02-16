from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import *
from part.models import *
from warehouse.models import *
from .forms import *

# Create your views here.

def hub(request):
    return render(request, "hub/hub.html", context={"symbol":"Logo", "fields":['Check_in', 'Check_out', 'Part', 'Shelf', 'Storage', 'Warehouse', 'Location', 'Search'], "type":Type.objects.all()})

def locations(request):
    if request.method == "POST":
        l = Form_location(request.POST)
        if l.is_valid():
            location = l.save()
            location.save()
    else:
        form =Form_location()
    return render(request, "hub/locations.html", context={"list":Location.objects.all(), "form":[Form_location]})

def results(request):
    if request.method == "GET":
        if request.GET['type']=="part":
            if request.GET['search'] == "NONE":
                r = Part.objects.filter(template__pType__tName__exact=request.GET["ptype"])
            else:
                r = Part.objects.filter(template__name__contains=request.GET['search'], template__pType__tName__exact=request.GET["ptype"])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"part"})

        elif request.GET['type']=="warehouse":
            if request.GET['search'] == "NONE":
                r = Warehouse.objects.all()
            else:
                r = Warehouse.objects.filter(name__contains=request.GET['search'])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"warehouse"})

        elif request.GET['type']=="storage":
            if request.GET['search'] == "NONE":
                r = Storage.objects.all()
            else:
                r = Storage.objects.filter(name__contains=request.GET['search'])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"storage"})

        elif request.GET['type']=="shelf":
            if request.GET['search'] == "NONE":
                r = Shelf.objects.all()
            else:
                r = Shelf.objects.filter(code__contains=request.GET['search'])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"shelf"})

        elif request.GET['type']=="location":
            if request.GET['search'] == "NONE":
                r = Location.objects.all()
            else:
                r = Location.objects.filter(name__contains=request.GET['search'])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"location"})
