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

