from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from .models import Location
from .forms import Form_location

# Create your views here.

def hub(request):
    return render(request, "hub/hub.html")

def manage(request):
    return render(request, "hub/manage.html")

def locations(request):
    if request.method == "POST":
        form = Form_location(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            location = Location.objects.create()
            location.name = form.cleaned_data['name']
            location.traditional_land = form.cleaned_data['traditional_land']
            location.traditional_country = form.cleaned_data['traditional_country']
            location.traditional_city = form.cleaned_data['traditional_city']
            location.traditional_zipcode = form.cleaned_data['traditional_zipcode']
            location.traditional_street = form.cleaned_data['traditional_street']
            location.traditional_street_number = form.cleaned_data['traditional_street_number']

            location.save()
    else:
        form =Form_location()
    return render(request, "hub/location.html", context={"list":Location.objects.all(), "form":Form_location, "add":"Standort Hinzufügen"})
