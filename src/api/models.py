from django.db import models
from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=100)
    phone_nr = models.IntegerField(max_length=15)
    email = models.EmailField(max_length=40)
