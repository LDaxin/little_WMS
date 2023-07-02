from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/accounts/login/')
def labels(request, typ):
    t = ArticleType.objects.get(lowerName__exact=typ)

    if t == None:
         return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return render(request, "hub/modules/items.html", context={"symbol":t.tSymbol, "searchFieldName":"articleSearch" + t.tName, 'type':"article", "name":typ, "form":[FormTemplateArticle(typ=t), FormArticleBase(typ=t)],  "typ":typ})
