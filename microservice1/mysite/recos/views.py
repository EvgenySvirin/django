from django.http import HttpResponse
from django.utils import timezone

from .models import Recom


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, choice_id):
    query = (
        Recom.objects.filter(choice_id=choice_id)
        .order_by("-pub_date")
        .filter(pub_date__lte=timezone.now())
    )

    content = "No recommendation"
    if len(query) != 0:
        content = query[0].recom_text
    return HttpResponse(content=content)
