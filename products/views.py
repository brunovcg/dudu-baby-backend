from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from products.models import Products
from products.serializers import ProductsSerializer
from django.db import IntegrityError
from accounts.models import User
from accounts.permissions import IsSuperuser
from django.shortcuts import get_object_or_404
from categories.models import Categories

class ProductsView(APIView):

  def delete(self, request, product_id=""):
    products = Products.objects.all()
    products.delete()
    return Response({"Message": "All products deleted"},status=status.HTTP_200_OK)

  def get (self, request):
    products = Products.objects.all()
    serialized =  ProductsSerializer(products, many=True)
    return Response(serialized.data,status=status.HTTP_200_OK)

  def post(self, request):
     try:
        message = request.data["message"]
     except KeyError:
        message = None

     try:
        category = request.data["category"]
     except KeyError:
        return Response({"You need to pass a category"},status=status.HTTP_400_BAD_REQUEST)

     category = Categories.objects.get_or_create(name=request.data["name"])[0]

     try:
       new_product =  Products.objects.create(
           name = request.data["name"],
           status = False,
           link = request.data["link"],
           img= request.data["img"],
           person= request.data["person"],
           price= request.data["price"],
           message = message,
           category = category
         
            )
     except IntegrityError:
            return Response({"Error on payload"},status=status.HTTP_400_BAD_REQUEST)


     serialized = ProductsSerializer(new_product)
     return Response(serialized.data, status=status.HTTP_201_CREATED)


class ProductOneView(APIView):

  def patch(self, request, product_id=""):

      if not request.data:
        return Response({"message": "You sent no options to update"},status=status.HTTP_400_BAD_REQUEST)

      product = get_object_or_404(Products, id= product_id)
      serialized =  ProductsSerializer(product, request.data, partial=True)
      if serialized.is_valid():
        serialized.save()

      return Response(serialized.data,status=status.HTTP_200_OK)

  def delete(self, request, product_id=""):
    product = get_object_or_404(Products,id=product_id)
    product.delete()
    return Response({"Message":f"Deleted {product_id} categories"},status=status.HTTP_200_OK)
  
  
class MassiveLoadView(APIView):
  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsSuperuser]


  def post(self, request):
    products = Products.objects.all()
    products.delete()


    for product in request.data:

      # try:
      #   message = product["message"]
      # except KeyError:
      #   message = None

      # try:
      #   category = product["category"]
      # except KeyError:
      #   return Response({"You need to pass a category"},status=status.HTTP_400_BAD_REQUEST)

      category = Categories.objects.get_or_create(name=product["name"])[0].id
      
      each_product = {
        "name" : product["name"],
        "link" : product["link"],
        "img" : product["img"],
        "price": product["price"],
        "message" :  product["message"],
        "person": product["person"],
        "status": False,
        "category": category
      }

      serialized = ProductsSerializer( data = each_product)

      if serialized.is_valid():
           product = serialized.save()
      else:
         print(each_product)

    
    products = Products.objects.all()

    products_serialized = ProductsSerializer( products, many=True)
    
    return Response({"message" : "done", "data" : products_serialized .data}, status=status.HTTP_201_CREATED)
      
