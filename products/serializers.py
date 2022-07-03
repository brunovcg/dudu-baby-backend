from rest_framework import serializers
from .models import Products
from categories.serializers import CategoriesSerializer


class ProductsSerializer(serializers.ModelSerializer):

  category = CategoriesSerializer()

  class Meta:
    model = Products
    fields = ["id","name", "status", "link", "img","price", "message", "person", "category"]


