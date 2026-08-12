from django.utils import timezone
from rest_framework import serializers

from accounts.models import Parent
from lsas.models import LSAProfile

from .models import BookingRequest


class BookingRequestSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent",
        queryset=Parent.objects.all(),
        write_only=True,
    )

    lsa_id = serializers.PrimaryKeyRelatedField(
        source="lsa",
        queryset=LSAProfile.objects.filter(is_active=True),
        write_only=True,
    )

    class Meta:
        model = BookingRequest
        fields = [
            "id",
            "parent_id",
            "lsa_id",
            "start_time",
            "end_time",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        start_time = attrs["start_time"]
        end_time = attrs["end_time"]

        if start_time >= end_time:
            raise serializers.ValidationError(
                {
                    "end_time":
                    "End time must be after start time."
                }
            )

        if start_time <= timezone.now():
            raise serializers.ValidationError(
                {
                    "start_time":
                    "Booking must be in the future."
                }
            )

        return attrs