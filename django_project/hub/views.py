from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import *
import article.models as ar
#from storage.models import *
import storage.models as st
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.




@login_required(login_url='/accounts/login/')
def hub(request):
    return render(request, "hub/hub.html", context={"symbol":"Logo", "fields":['Check_in', 'Check_out', 'Article', 'Storage'], "paType":ar.ArticleType.objects.all(), "stType":st.StorageType.objects.all()})





@login_required(login_url='/accounts/login/')
def locations(request):
    return render(request, "hub/locations.html", context={"list":Location.objects.all(), "form":[Form_location]})

@login_required(login_url='/accounts/login/')
def delLocation(request):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Location.objects.filter(pk=value).first()
                    delList.append(pa)
                except Exception as e:
                    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":e, "toastType":"alert"})
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()

        return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastText":delListReturn, "toastType":"alert"})

    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})


@login_required(login_url='/accounts/login/')
def addLocation(request):
    if request.method == "POST":
        l = Form_location(request.POST)
        if l.is_valid():
            location = l.save()
            location.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastText":str(location) + " was added to your system.", "toastType":"status"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastText":"thomething went wrong", "toastType":"alert"})




@login_required(login_url='/accounts/login/')
def results(request):
    if request.method == "GET":
        if request.GET['type']=="article":
            if request.GET['search'] == "NONE":
                r = ar.Article.objects.filter(template__pType__tName__exact=request.GET["ptype"])
            else:
                #r = Article.objects.filter(template__name__contains=request.GET['search'], template__pType__tName__exact=request.GET["ptype"])

                r = ar.Article.objects.filter(Q(template__name__contains=request.GET['search']) | Q(code__contains=request.GET['search']), template__pType__tName__exact=request.GET["ptype"])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})

        elif request.GET['type']=="storage":
            if request.GET['search'] == "NONE":
                r = Storage.objects.all()
            else:
                r = Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__contains=request.GET['search']))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"storage"})

        elif request.GET['type']=="storage":
            if request.GET['search'] == "NONE":
                r = Storage.objects.all()
            else:
                r = Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__contains=request.GET['search']))
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
                r = Location.objects.filter(Q(code__contains=request.GET['search']))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"location"})
