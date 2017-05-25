from django.contrib import admin
from billing import models

@admin.register(models.Plan)
class PlanAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
    
# admin.site.register(models.Subscription, SubscriptionAdmin)
#
# class EndpointCallBillingAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(models.EndpointCallBilling, EndpointCallBillingAdmin)
#
# class EndpointPlanBillingAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(models.EndpointPlanBilling, EndpointPlanBillingAdmin)
