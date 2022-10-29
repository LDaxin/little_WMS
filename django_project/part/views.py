from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def part(request):
    if request.method == "POST":
        p = Form_part(request.POST)
        if p.is_valid():
            part = p.save()
            part.save()
    else:
        form_p = Form_part()
        Form_c = Form_container()
    return render(request, "part/part.html", context={"list":Part.objects.all(), "form":[[Form_part],[Form_container]]})

def tag(request):
    if request.method == "POST":
        t = Form_tag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "part/tag.html", context={"list":Tag.objects.all(), "form":[[Form_tag]]})
