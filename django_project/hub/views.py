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
    return render(request, "hub/hub.html", context={"symbol":"Logo", "fields":['movement', 'Article', 'Storage', 'Location'], "paType":ar.ArticleType.objects.all(), "stType":st.StorageType.objects.all()})

@login_required(login_url='/accounts/login/')
def results(request):
    if request.method == "GET":
        if request.GET['type']=="article":
            if request.GET['search'] == "NONE":
                r = ar.Article.objects.filter(template__pType__lowerName__exact=request.GET["ptype"])
            else:
                #r = Article.objects.filter(template__name__contains=request.GET['search'], template__pType__tName__exact=request.GET["ptype"])

                r = ar.Article.objects.filter(Q(template__name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), template__pType__lowerName__exact=request.GET["ptype"])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})

        elif request.GET['type']=="storage":
            if request.GET['search'] == "NONE":
                r = st.Storage.objects.all()
            else:
                r = st.Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"storage"})

