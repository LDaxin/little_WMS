from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
from .forms import Form_location
from part.models import *
from part.forms import *

# Create your views here.

def hub(request):
    return render(request, "hub/hub.html")

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

def part(request):
    if request.method == "POST":
        p = Form_part(request.POST)
        if p.is_valid():
            part = p.save()
            part.save()
    else:
        form_p = Form_part()
        Form_c = Form_container()
    return render(request, "hub/part.html", context={"list":Part.objects.all(), "form":[[Form_part],[Form_container]]})

def tag(request):
    if request.method == "POST":
        t = Form_tag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "hub/tag.html", context={"list":Tag.objects.all(), "form":[[Form_tag]]})
