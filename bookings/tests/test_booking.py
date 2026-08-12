from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import Parent
from lsas.models import LSAProfile, Skill
from bookings.models import BookingRequest


@pytest.fixture
def parent():
    return Parent.objects.create(
        name="Rahul Kumar",
        email="rahul.test@example.com",
        phone="9876543210",
    )


@pytest.fixture
def lsa():
    skill = Skill.objects.create(name="Autism")

    lsa = LSAProfile.objects.create(
        name="Priya Sharma",
        email="priya.booking@example.com",
        is_active=True,
    )
    lsa.skills.add(skill)

    return lsa


@pytest.mark.django_db
def test_successful_booking(parent, lsa):
    client = APIClient()

    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=1)

    response = client.post(
        "/api/v1/bookings/",
        {
            "parent_id": parent.id,
            "lsa_id": lsa.id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["status"] == "PENDING"


@pytest.mark.django_db
def test_invalid_booking_time(parent, lsa):
    client = APIClient()

    start = timezone.now() + timedelta(days=1)
    end = start - timedelta(hours=1)

    response = client.post(
        "/api/v1/bookings/",
        {
            "parent_id": parent.id,
            "lsa_id": lsa.id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_overlapping_booking_is_rejected(parent, lsa):
    client = APIClient()

    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=1)

    first = client.post(
        "/api/v1/bookings/",
        {
            "parent_id": parent.id,
            "lsa_id": lsa.id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
        },
        format="json",
    )

    assert first.status_code == 201

    second = client.post(
        "/api/v1/bookings/",
        {
            "parent_id": parent.id,
            "lsa_id": lsa.id,
            "start_time": (start + timedelta(minutes=30)).isoformat(),
            "end_time": (end + timedelta(minutes=30)).isoformat(),
        },
        format="json",
    )

    assert second.status_code == 409