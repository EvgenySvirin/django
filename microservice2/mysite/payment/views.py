from django.http import HttpResponse

from .models import Payment


def index(request):
    return HttpResponse("Hello, world. You're at the payment index.")


def detail(request, username):
    query = Payment.objects.filter(username=username)
    content = -1
    if len(query) != 0 and 0 < query[0].debt:
        content = query[0].debt
    return HttpResponse(content=content)
