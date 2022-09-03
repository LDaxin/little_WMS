from urllib import response
from django.shortcuts import render
from django.http import HttpResponse
from hub.models import Location
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
            location.traditional_land = form.cleaned_data['land']
            location.traditional_country = form.cleaned_data['country']
            location.traditional_city = form.cleaned_data['city']
            location.traditional_zipcode = form.cleaned_data['zipcode']
            location.traditional_street = form.cleaned_data['street']
            location.traditional_street_number = form.cleaned_data['street_number']

            location.save()
    else:
        form =Form_location()
    return render(request, "hub/locations.html", context={"location":Location.objects.all(), "form":Form_location}, )
