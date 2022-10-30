from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def part(request):
    if request.method == "POST":
        t = FormTemplatePart(request.POST)
        if t.is_valid():
            template = t.save()
            template.save()
    return render(request, "part/part.html", context={"list":Part.objects.all(), "form":[[FormTemplatePart],[FormTemplateContainer]]})

def tag(request):
    if request.method == "POST":
        t = FormTag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "part/tag.html", context={"list":Tag.objects.all(), "form":[[FormTag]]})
