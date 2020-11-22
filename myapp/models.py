from django.db import models
from datetime import datetime

# Create your models here.

class Send(models.Model):
    to = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.subject


class Recieve(models.Model):
    subject = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    get_by = models.CharField(max_length=200, default="")
    message = models.TextField()


    def __str__(self):
        return self.subject
