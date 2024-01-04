from django.urls import path

from . import views

app_name = "recos"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:choice_id>/", views.detail, name="detail"),
]
