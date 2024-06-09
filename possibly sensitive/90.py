import json
from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from django.utils import timezone
from requests import HTTPError

from .. import PaymentError
from .. import PaymentStatus
from .. import PurchasedItem
from .. import RedirectNeeded
from . import PaypalCardProvider
from . import PaypalProvider

CLIENT_ID = "abc123"
PAYMENT_TOKEN = "5a4dae68-2715-4b1e-8bb2-2c2dbe9255f6"
SECRET = "123abc"
VARIANT = "wallet"

PROCESS_DATA = {
    "name": "John Doe",
    "number": "371449635398431",
    "expiration_0": "5",
    "expiration_1": "2023",
    "cvv2": "1234",
}


class Payment(Mock):
    id = 1
    description = "payment"
    currency = "USD"
    delivery = Decimal(10)
    status = PaymentStatus.WAITING
    tax = Decimal(10)
    token = PAYMENT_TOKEN
    total = Decimal(220)
    captured_amount = Decimal(0)
    variant = VARIANT
    transaction_id = None
    message = ""
    extra_data = json.dumps(
        {
            "links": {
                "approval_url": None,
                "capture": {"href": "http://capture.com"},
                "refund": {"href": "http://refund.com"},
                "execute": {"href": "http://execute.com"},
            }
        }
    )

    def change_status(self, status, message=""):
        self.status = status
        self.message = message

    def get_failure_url(self):
        return "http://cancel.com"

    def get_process_url(self):
        return "http://example.com"

    def get_purchased_items(self):
        return [
            PurchasedItem(