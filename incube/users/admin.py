from django.contrib import admin
from users import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(models.StripeAccount)
class StripeAccountAdmin(admin.ModelAdmin):
    pass
