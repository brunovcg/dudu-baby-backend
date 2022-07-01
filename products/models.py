from django.db import models
from categories.models import Categories

class Products (models.Model):
   name = models.CharField(max_length=255, null=False)
   price = models.FloatField(max_length=255, null=False)
   link = models.CharField(max_length=255, null=False)
   img = models.CharField(max_length=255, null=False)
   status = models.BooleanField(null=False)
   person = models.CharField(max_length=255, null=False)
   message = models.CharField(max_length=255, null=True, blank=True)
   category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categories")
   