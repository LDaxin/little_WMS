from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hub(request):
    return render(request, "hub/header.html")

