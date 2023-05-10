from django.shortcuts import render
from storage.models import Storage
from article.models import Article
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

@login_required(login_url='/accounts/login/')
def movement(request):

    return render(request, "movement/movement.html")


@login_required(login_url='/accounts/login/')
def movementCodeInfo(request):
    if request.method == "GET":
        if request.GET['code'][0:2] == "a0":
            try:
                article = Article.objects.get(code__code__exact=request.GET['code'])
            except ObjectDoesNotExist:
                return JsonResponse({"name": "bla2"})

            returnJson = {"name":article.template.name, "code":article.code.code, "storable":True, "storage":article.template.pType.ref}
            return JsonResponse(returnJson)

        elif request.GET['code'][0:2] == "s0":
            try:
                storage = Storage.objects.get(code__code__exact=request.GET['code'])
            except ObjectDoesNotExist:
                return JsonResponse({"name": "bla2"})

            returnJson = {"name":storage.name, "code":storage.code.code, "storable":False, "storage":True}
            return JsonResponse(returnJson)

             #code storable storage name


        return JsonResponse({"name": "bla"})
    return JsonResponse({"foo":"nonononono"})

