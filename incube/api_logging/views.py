from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsApiOwner

from api_logging.models import APILogEntry
from api_logging.serializers import APILogEntrySerializer

class LogDetailView(RetrieveAPIView):
    serializer_class = APILogEntrySerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return models.APILogEntry.objects\
            .filter(api__owner=self.request.user.id)
