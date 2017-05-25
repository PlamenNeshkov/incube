from subdomains.middleware import SubdomainURLRoutingMiddleware

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class IncubeSubdomainMiddleware(SubdomainURLRoutingMiddleware, MiddlewareMixin):
    pass
