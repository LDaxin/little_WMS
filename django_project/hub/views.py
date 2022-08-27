from django.shortcuts import render
from django.http import HttpResponse
from hub.models import Location

# Create your views here.

def hub(request):
    return render(request, "hub/hub.html")

def manage(request):
    return render(request, "hub/manage.html")

def locations(request):

    return render(request, "hub/locations.html", context={"location":Location.objects.all()})
