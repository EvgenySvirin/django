import datetime

from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Payment


def create_payment(username, debt):
    """
    Create payment with given username and debt
    """
    return Payment.objects.create(username=username, debt=debt)


class DetailViewTests(TestCase):
    def test_existing_recom(self):
        """
        Payment corresponding to username exists in database
        """
        recom = create_payment(username="john", debt=1000)
        url = reverse("payment:detail", args=("john",))
        res = self.client.get(url).content.decode("utf-8")
        self.assertEqual("1000", res)

    def test_no_recom(self):
        """
        Payment corresponding to username does not exist in database
        """
        url = reverse("payment:detail", args=("john",))
        res = self.client.get(url).content.decode("utf-8")
        self.assertEqual("-1", res)
