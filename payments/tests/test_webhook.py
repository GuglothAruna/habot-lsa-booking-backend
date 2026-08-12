from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import Parent
from bookings.models import BookingRequest
from lsas.models import LSAProfile
from payments.models import Payment


@pytest.fixture
def booking():
    parent = Parent.objects.create(
        name="Sita Kumar",
        email="sita.test@example.com",
    )

    lsa = LSAProfile.objects.create(
        name="Ravi Kumar",
        email="ravi.payment@example.com",
        is_active=True,
    )

    start = timezone.now() + timedelta(days=2)
    end = start + timedelta(hours=1)

    booking = BookingRequest.objects.create(
        parent=parent,
        lsa=lsa,
        start_time=start,
        end_time=end,
        status=BookingRequest.Status.PENDING,
    )

    Payment.objects.create(
        booking=booking,
        amount=500,
        status=Payment.Status.PENDING,
    )

    return booking


@pytest.mark.django_db
def test_payment_success_confirms_booking(booking):
    client = APIClient()

    response = client.post(
        "/api/v1/payments/webhook/",
        {
            "booking_id": booking.id,
            "payment_status": "success",
            "transaction_id": "TXN-TEST-001",
        },
        format="json",
    )

    assert response.status_code == 200

    booking.refresh_from_db()
    payment = booking.payment

    assert booking.status == BookingRequest.Status.CONFIRMED
    assert payment.status == Payment.Status.SUCCESS
    assert payment.transaction_id == "TXN-TEST-001"


@pytest.mark.django_db
def test_invalid_webhook_payload(booking):
    client = APIClient()

    response = client.post(
        "/api/v1/payments/webhook/",
        {},
        format="json",
    )

    assert response.status_code == 400
@pytest.mark.django_db
def test_duplicate_success_webhook_is_safe(booking):
    client = APIClient()

    payload = {
        "booking_id": booking.id,
        "payment_status": "success",
        "transaction_id": "TXN-DUPLICATE",
    }

    first_response = client.post(
        "/api/v1/payments/webhook/",
        payload,
        format="json",
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/payments/webhook/",
        payload,
        format="json",
    )

    assert second_response.status_code == 200
    assert second_response.data["detail"] == "Payment already processed."