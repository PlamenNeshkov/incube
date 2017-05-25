from django.contrib import admin
from api_auth import models

class AuthMethodAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.AuthMethod, AuthMethodAdmin)

class BasicAuthCredentialsAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.BasicAuthCredentials, BasicAuthCredentialsAdmin)

class KeyCredentialsAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.KeyCredentials, KeyCredentialsAdmin)

class AcceptedKeyParameterAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.AcceptedKeyParameter, AcceptedKeyParameterAdmin)
