from django.conf import settings
from payments.models import Payment
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lsas.models import LSAProfile

from .models import BookingRequest
from .serializers import BookingRequestSerializer


class BookingCreateView(APIView):
    """
    Create a booking while preventing overlapping sessions.

    Concurrency protection:
    - Locks the selected LSA row inside a database transaction.
    - Checks for overlapping active bookings.
    - Creates the booking only when the slot is available.
    """

    @transaction.atomic
    def post(self, request):
        serializer = BookingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parent = serializer.validated_data["parent"]
        lsa = serializer.validated_data["lsa"]
        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]

        # Lock the LSA row so concurrent booking requests
        # for the same LSA are processed safely.
        lsa = (
            LSAProfile.objects
            .select_for_update()
            .get(pk=lsa.pk)
        )

        # Double-booking check.
        overlapping_booking = (
            BookingRequest.objects
            .filter(
                lsa=lsa,
                status__in=[
                    BookingRequest.Status.PENDING,
                    BookingRequest.Status.CONFIRMED,
                ],
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            .exists()
        )

        if overlapping_booking:
            return Response(
                {
                    "detail": (
                        "This LSA is already booked "
                        "during the requested time."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        booking = BookingRequest.objects.create(
            parent=parent,
            lsa=lsa,
            start_time=start_time,
            end_time=end_time,
            status=BookingRequest.Status.PENDING,
        )
        Payment.objects.create(
    booking=booking,
    amount=settings.DEFAULT_SESSION_FEE,
    status=Payment.Status.PENDING,
)

        return Response(
            BookingRequestSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )