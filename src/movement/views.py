from django.shortcuts import render
from django.template.loader import render_to_string
from storage.models import Storage
from article.models import Article
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.

@login_required(login_url='/accounts/login/')
def movement(request):

    return render(request, "movement/movement.html")


@login_required(login_url='/accounts/login/')
def movementRemove(request):
    if request.method == "POST":

        articleObject = Article.objects.get(code__code__exact = request.POST["articleCode1"])
        articleObject.stored = None
        articleObject.save()

        context = {
            "toastName":"Success",
            "toastId":"successToast",
            "toastText":"success fully removed " + articleObject.base.name,
            "toastType":"success"
        }

        return render(request, "hub/modules/toast.html", context=context)

    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":'what are you trying to do', "toastType":"alert"})


@login_required(login_url='/accounts/login/')
def movementStore(request):
    if request.method == "POST":
        hallo = []
        if request.POST["storageCode"].startswith("s0"):
            storageObject = Storage.objects.get(code__code__exact = request.POST["storageCode"])
        elif request.POST["storageCode"].startswith("a0"):
            storageObject = Article.objects.get(code__code__exact = request.POST["storageCode"])

        for formField in request.POST:
            if formField.startswith('articleCode'):
                articleObject = Article.objects.get(code__code__exact = request.POST[formField])
                articleObject.stored = storageObject.space
                articleObject.save()
                hallo.append(articleObject)

        return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":str(hallo), "toastType":"alert"})
    return render(request, "hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":'what are you trying to do', "toastType":"alert"})


@login_required(login_url='/accounts/login/')
def movementCodeInfo(request):
    if request.method == "GET":
        if request.GET['code'][0:2] == "a0":
            try:
                article = Article.objects.get(code__code__exact=request.GET['code'])
            except ObjectDoesNotExist:
                return JsonResponse({"error":"no such a article in the System", "errorToast":render_to_string("hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"no such a article in the System", "toastType":"alert"})})

            returnJson = {"error":"", "name":article.base.name, "code":article.code.code, "storable":True, "storage":False, "space":article.space.active}
            return JsonResponse(returnJson)

        elif request.GET['code'][0:2] == "s0":
            try:
                storage = Storage.objects.get(code__code__exact=request.GET['code'])
            except ObjectDoesNotExist:
                return JsonResponse({"error":"no such a storage in the System", "errorToast":render_to_string("hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"no such a storage in the System", "toastType":"alert"})})

            returnJson = {"error":"", "name":storage.name, "code":storage.code.code, "storable":False, "storage":True, "space":True}
            return JsonResponse(returnJson)

             #code storable storage name


        return JsonResponse({"error":"not a valide code", "errorToast":render_to_string("hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"not a valide code", "toastType":"alert"})})
    return JsonResponse({"error":"what are you trying to do?", "errorToast":render_to_string("hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"what are you trying to do?", "toastType":"alert"})})

@login_required(login_url='/accounts/login/')
def movementSearch(request):
    if request.method == "GET":
        if request.GET['search'] == "":
            ra = Article.objects.filter(base__name__exact="")
            rs = Storage.objects.filter(name__exact="")
            return render(request, "hub/modules/quickResults.html", context={"resultsA":ra, "resultsS":rs})
        else:
            ra = Article.objects.filter(Q(base__name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']))
            rs = Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']))
            return render(request, "hub/modules/quickResults.html", context={"resultsA":ra, "resultsS":rs})
    return JsonResponse({"error":"what are you trying to do?", "errorToast":render_to_string("hub/modules/toast.html", context={"toastName":"Error", "toastId":"errorToast", "toastText":"what are you trying to do?", "toastType":"alert"})})

