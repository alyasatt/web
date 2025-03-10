
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def str(self):
        return self.name
# Create your models here.
