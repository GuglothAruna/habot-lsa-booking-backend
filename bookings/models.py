from django.db import models

from accounts.models import Parent
from lsas.models import LSAProfile


class BookingRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PAYMENT_FAILED = "PAYMENT_FAILED", "Payment Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    parent = models.ForeignKey(
        Parent,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    lsa = models.ForeignKey(
        LSAProfile,
        on_delete=models.PROTECT,
        related_name="bookings",
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["lsa", "start_time", "end_time"]
            ),
            models.Index(
                fields=["status", "start_time"]
            ),
        ]

    def __str__(self):
        return f"Booking {self.id}"