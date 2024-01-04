import datetime

from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Recom


def create_recommendation(recom_text, days, choice_id):
    """
    Create recommendation with given text, days from current date and choice id
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Recom.objects.create(
        recom_text=recom_text, pub_date=time, choice_id=choice_id
    )


class DetailViewTests(TestCase):
    def test_existing_recom(self):
        """
        Recommendation corresponding to choice id exists in database
        """
        recom = create_recommendation(recom_text="Something", days=-5, choice_id=1)
        url = reverse("recos:detail", args=(1,))
        res = self.client.get(url).content.decode("utf-8")
        self.assertEqual("Something", res)

    def test_no_recom(self):
        """
        Recommendation corresponding to choice id does not exist in database
        """
        url = reverse("recos:detail", args=(1,))
        res = self.client.get(url).content.decode("utf-8")
        self.assertEqual("No recommendation", res)
