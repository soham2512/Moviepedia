from django.db import models


class Order(models.Model):
    imdbID = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True)
    amount = models.IntegerField(blank=True)
    currency = models.CharField(max_length=200, blank=True)
    transactionId = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username
