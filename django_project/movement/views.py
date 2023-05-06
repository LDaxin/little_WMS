from django.shortcuts import render
from storage.models import Storage
from article.models import Article
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/accounts/login/')
def movement(request):

    return render(request, "movement/movement.html")
