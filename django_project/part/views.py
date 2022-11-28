from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def part(request):
    if request.method == "POST":
        if 'add_1' in request.POST:
            t = FormTemplatePart(request.POST)
            if t.is_valid():
                template = t.save()
                part = Part(template=template)
                template.save()
                part.save()
        elif 'add_2' in request.POST:
            t = FormTemplateContainer(request.POST)
            if t.is_valid():
                template = t.save()
                part = Part(template=template)
                template.save()
                part.save()

        elif 'add_3' in request.POST:
            p = FormPartBase(request.POST)
            if p.is_valid():
                part = p.save()
                part.save()
    return render(request, "part/part.html", context={"symbol":"Part", "list":Part.objects.all(), "form":[[FormTemplatePart],[FormTemplateContainer],[FormPartBase]]})

def tag(request):
    if request.method == "POST":
        t = FormTag(request.POST)
        if t.is_valid():
            tag = t.save()
            tag.save()
    return render(request, "part/tag.html", context={"list":Tag.objects.all(), "form":[[FormTag]]})
