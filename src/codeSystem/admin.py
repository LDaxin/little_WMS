from django.contrib import admin
from codeSystem.models import *

class MuidCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('muidCodePretty',)

# Register your models here.
admin.site.register(MuidCode)
