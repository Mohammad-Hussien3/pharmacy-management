from django.db import models

# Create your models here.

class Product(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + str(self.quantity)
