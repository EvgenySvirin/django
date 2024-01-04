from django.db import models


class Recom(models.Model):
    recom_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    choice_id = models.IntegerField(default=0)
