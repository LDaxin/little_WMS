from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q

# Create your views here.

@login_required(login_url='/accounts/login/')
def tag(request, tagId):
    try:
        tagObject = Tag.objects.get(pk=tagId)
        tagForm = FormChangeTag(instance=tagObject)
        return render(request, "hub/modules/item.html", context={"symbol":"Tag", "searchFieldName":"tagSearch", "id":tagId, "modalId":"single", "form":[tagForm], "actionType":"update"})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    

def tagIncert(request, tagId):
    try:
        tagObject = Tag.objects.get(pk=tagId)
        tagForm = FormChangeTag(instance=tagObject)
        return render(request, "hub/modules/itemForm.html", context={"searchFieldName":"tagSearch",  "id":tagId, "modalId":"single", "form":[tagForm], "actionType":"update"})
    except:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def tags(request):
    return render(request, "hub/modules/items.html", context={"symbol":"Tag", "searchFieldName":"tagSearch", 'type':"tag", "name":"tag", "form":[FormTag], "modalId":"add"})

def addTag(request):
    if request.method == "POST":
        tagForm = FormTag(request.POST)
        if tagForm.is_valid():
            tag = tagForm.save()
            tag.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Add Succses", "toastId":"successToast", "toastText":str(tag) + " was added to your system.", "toastType":"status"})

def delTag(request):
    if request.method == "POST":
        delList = []
        delListReturn = ""
        for key, value in request.POST.items():
            if key[0:1] == '_':
                try:
                    pa = Tag.objects.filter(pk=value).first()
                    delList.append(pa)
                except Exception as e:
                    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":e, "toastType":"alert"})
        for i in delList:
            delListReturn = delListReturn + i.__str__() + " "
            i.deleted = True
            i.save()
        return render(request, "hub/modules/toast.html", context={"toastName":"Delete", "toastId":"successToast", "toastText":delListReturn, "toastType":"alert"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"thomething went wrong", "toastType":"alert"})






def updateTag(request, tagId):
    tagObject = Tag.objects.get(pk=tagId)

    if request.method == "POST":
        tagForm = FormTag(request.POST, instance=tagObject)
        if tagForm.is_valid():
            tagForm.save()
            return render(request, "hub/modules/toast.html", context={"toastName":"Update Succses", "toastId":"successToast", "toastText":"Tag was updated.", "toastType":"status"})

@login_required(login_url='/accounts/login/')
def searchTags(request):
    if request.method == "GET":
        if request.GET['search'] == "":
            r = Tag.objects.all()
        else:
            r = Tag.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']))
        return render(request, "hub/modules/results.html", context={"results":r, "type":"tag"})
