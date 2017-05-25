from rest_framework.permissions import BasePermission

class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsStripeConnected(BasePermission):
    message = 'You must be connected to Stripe to do this.'

    def has_permission(self, request, view):
        return getattr(request.user, 'stripe_account', None) != None

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsApiOwner(BasePermission):
    message = 'You must own the related API to do this.'

    def has_object_permission(self, request, view, obj):
        return obj.api.owner == request.user

class IsPlanOwner(BasePermission):
    message = 'You must own the related Plan to do this.'

    def has_object_permission(self, request, view, obj):
        return obj.plan.api.owner == request.user
