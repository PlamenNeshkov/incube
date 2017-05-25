from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsApiOwner, IsOwner
from stats import helpers, serializers
from api_logging.models import APILogEntry

from datetime import datetime

class APIStatsView(generics.GenericAPIView):
    serializer_class = serializers.APIStatsSerializer
    permission_classes = (IsAuthenticated, IsApiOwner)

    def get_queryset(self):
        return APILogEntry.objects\
            .filter(api=self.kwargs['pk'], api__owner=self.request.user.id)

    def get(self, request, pk=None):
        log_entries = self.get_queryset()
        now = datetime.now()

        minute_calls = helpers.minute_calls(log_entries, now)
        hourly = helpers.hourly_calls_by_minute(log_entries, now)
        daily = helpers.daily_calls_by_hour(log_entries, now)
        monthly = helpers.monthly_calls_by_day(log_entries, now)
        yearly = helpers.yearly_calls_by_month(log_entries, now)

        data = {
            'average_latency': helpers.average_latency(log_entries),
            'unique_consumers': helpers.unique_consumers(log_entries),
            'all_time_calls': helpers.all_time_calls(log_entries),
            'calls_by_minute': hourly[0],
            'calls_by_hour': daily[0],
            'calls_by_day': monthly[0],
            'calls_by_month': yearly[0],
            'minute_calls': minute_calls,
            'hourly_calls': hourly[1],
            'daily_calls': daily[1],
            'monthly_calls': monthly[1],
            'yearly_calls': yearly[1],
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)
