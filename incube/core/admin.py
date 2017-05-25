from django.contrib import admin
from core import models

class APIAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.API, APIAdmin)

class ConsumerAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Consumer, ConsumerAdmin)
