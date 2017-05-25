from rest_framework import serializers

class APIStatsSerializer(serializers.Serializer):
    average_latency = serializers.IntegerField()
    unique_consumers = serializers.IntegerField()
    all_time_calls = serializers.IntegerField()

    calls_by_minute = serializers.DictField()
    calls_by_hour = serializers.DictField()
    calls_by_day = serializers.DictField()
    calls_by_month = serializers.DictField()

    minute_calls = serializers.IntegerField()
    hourly_calls = serializers.IntegerField()
    daily_calls = serializers.IntegerField()
    monthly_calls = serializers.IntegerField()
    yearly_calls = serializers.IntegerField()
