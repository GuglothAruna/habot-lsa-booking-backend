from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import BookingRequest
from .models import Payment


class PaymentWebhookView(APIView):
    
    @transaction.atomic
    def post(self, request):
        booking_id = request.data.get("booking_id")
        payment_status = request.data.get("payment_status")
        transaction_id = request.data.get("transaction_id")

        if not booking_id or payment_status not in {"success", "failure"}:
            return Response(
                {"detail": "Invalid webhook payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            booking = (
                BookingRequest.objects
                .select_for_update()
                .get(pk=booking_id)
            )
        except BookingRequest.DoesNotExist:
            return Response(
                {"detail": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            payment = (
                Payment.objects
                .select_for_update()
                .get(booking=booking)
            )
        except Payment.DoesNotExist:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if payment.status == Payment.Status.SUCCESS:
            return Response(
            {
                "detail": "Payment already processed.",
                "booking_id": booking.id,
                "booking_status": booking.status,
                "payment_status": payment.status,
            },
            status=status.HTTP_200_OK,
        )

        if payment_status == "success":
            payment.status = Payment.Status.SUCCESS
            payment.transaction_id = transaction_id
            booking.status = BookingRequest.Status.CONFIRMED
        else:
            payment.status = Payment.Status.FAILED
            booking.status = BookingRequest.Status.PAYMENT_FAILED

        payment.save(
            update_fields=["status", "transaction_id", "updated_at"]
        )

        booking.save(
            update_fields=["status", "updated_at"]
        )

        return Response(
            {
                "booking_id": booking.id,
                "booking_status": booking.status,
                "payment_status": payment.status,
            },
            status=status.HTTP_200_OK,
        )