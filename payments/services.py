import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class PaymentGatewayError(Exception):
    """Raised when the external payment gateway fails."""


class PaymentGatewayClient:
    def __init__(self):
        self.base_url = settings.PAYMENT_GATEWAY_URL

    def create_payment(self, booking_id, amount):
        payload = {
            "booking_id": booking_id,
            "amount": str(amount),
        }

        try:
            response = requests.post(
                self.base_url,
                json=payload,
                timeout=5,
            )

            response.raise_for_status()

            data = response.json()

            if data.get("status") != "success":
                raise PaymentGatewayError(
                    "Payment gateway returned a failed response."
                )

            return data

        except requests.RequestException as exc:
            logger.exception(
                "Payment gateway request failed for booking %s",
                booking_id,
            )
            raise PaymentGatewayError(
                "Payment gateway is unavailable."
            ) from exc