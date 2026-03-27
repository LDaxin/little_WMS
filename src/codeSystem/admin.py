from django.contrib import admin
from codeSystem.models import *

class UuidCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('uuidCode',)

# Register your models here.
admin.site.register(UuidCode)
