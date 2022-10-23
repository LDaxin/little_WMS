from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
from .forms import Form_location
from part.models import Part
from part.models import Tag
from part.forms import Form_part
from part.forms import Form_tag

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
    return render(request, "hub/location.html", context={"list":Location.objects.all(), "form":Form_location})

def part(request):
    return render(request, "hub/part.html", context={"list":Part.objects.all(), "form":Form_part})

def tag(request):
    return render(request, "hub/tag.html", context={"list":Tag.objects.all(), "form":Form_tag})
