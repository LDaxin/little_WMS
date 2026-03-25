from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from .forms import *
from space.models import Space
from django.contrib.auth.decorators import login_required

# Create your views here.
login_required(login_url='/accounts/login/')
def exportCSV(request):
    return render(request, "export/exportCSV.html", context={}, form=ExportCSVForm())


login_required(login_url='/accounts/login/')
def exportArticleSelect(request):
    return render(request, "export/exportSelect.html", context={}, form=ExportArticleSelectionForm())

login_required(login_url='/accounts/login/')
def exportArticleDefault(request):
    if request.method == "POST":

        pass
    return render(request, "export/exportDefault.html", context={}, form=ExportArticleSelectionForm())
