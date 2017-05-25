from django.db.models import Manager

class APIManager(Manager):
    def from_request(self, request):
        return super(APIManager, self)\
            .get_queryset()\
            .get(subdomain = request.subdomain)
