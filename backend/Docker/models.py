from django.db import models


class Docker(models.Model):
    conatiner_id = models.CharField(max_length=255)