from django.db import models


class Payment(models.Model):
    username = models.CharField(max_length=200)
    debt = models.IntegerField(default=0)
