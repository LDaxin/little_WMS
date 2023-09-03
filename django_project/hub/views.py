from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.template.loader import render_to_string
from .models import *
import article.models as ar
#from storage.models import *
import storage.models as st
import location.models as lo
import tag.models as ta
import codeSystem.models as co
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.




@login_required(login_url='/accounts/login/')
def hub(request):
    return render(request, "hub/hub.html", context={"symbol":"Logo", "fields":['movement', 'Article', 'Storage', 'Location', "Tag", "Code"], "paType":ar.ArticleType.objects.all(), "stType":st.StorageType.objects.all()})

@login_required(login_url='/accounts/login/')
def results(request):
    if request.method == "GET":
        if request.GET['type']=="article":
            if request.GET['search'] == "NONE":
                r = ar.Article.objects.filter(pType__lowerName__exact=request.GET["ptype"])
            else:
                #r = Article.objects.filter(name__contains=request.GET['search'], pType__tName__exact=request.GET["ptype"])

                r = ar.Article.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']), pType__lowerName__exact=request.GET["ptype"])
            return render(request, "hub/modules/results.html", context={"results":r, "type":"article"})

        elif request.GET['type']=="storage":
            if request.GET['search'] == "NONE":
                r = st.Storage.objects.all()
            else:
                r = st.Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"storage"})

        elif request.GET['type']=="location":
            if request.GET['search'] == "NONE":
                r = lo.Location.objects.all()
            else:
                r = lo.Storage.objects.filter(Q(name__contains=request.GET['search']) | Q(code__code__contains=request.GET['search']))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"location"})
        
        elif request.GET["type"]=="tag":
            if request.GET['search'] == "NONE":
                r = ta.Tag.objects.all()
            else:
                r = ta.Tag.objects.filter(Q(name__contains=request.GET['search']))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"tag"})

        elif request.GET["type"]=="code":
            if request.GET['search'] == "NONE":
                #r = co.UuidCode.objects.all()
                r = co.UuidCode.objects.filter(used=False)
            else:
                r = co.UuidCode.objects.filter(Q(code__contains=request.GET['search'])& Q(used=False))
            return render(request, "hub/modules/results.html", context={"results":r, "type":"code"})
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')
