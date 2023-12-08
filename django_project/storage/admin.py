from django.contrib import admin
from storage.models import *

# Register your models here.
admin.site.register(StorageType)
admin.site.register(Storage)
admin.site.register(Space)
