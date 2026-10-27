from django.contrib import admin
from article.models import *
from article.forms import ArticleTypeForm

# Register your models here.


class ArticleTypeAdmin(admin.ModelAdmin):
    form = ArticleTypeForm


admin.site.register(Article)
admin.site.register(ArticleType, ArticleTypeAdmin)
admin.site.register(ArticleBase)
admin.site.register(Tag)
