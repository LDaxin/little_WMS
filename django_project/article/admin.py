from django.contrib import admin
from article.models import *

# Register your models here.

admin.site.register(Article)
admin.site.register(ArticleType)
admin.site.register(Unit)
admin.site.register(Tag)
