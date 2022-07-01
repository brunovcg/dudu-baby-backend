from rest_framework.views import APIView
from categories.models import Categories
from categories.serializers import CategoriesSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsSuperuser, IsSuperuserAllowGetForAll

class CategoriesOneView(APIView):
  # authentication_classes = [TokenAuthentication]
  # permission_classes = [IsSuperuserAllowGetForAll]


  def delete(self, request, category_id):
    category = get_object_or_404(Categories,id=category_id)
    category.delete()
    return Response({"message" : f"category {category_id} deleted"},status=status.HTTP_200_OK)
  
  def patch(self, request, category_id):
     if not request.data:
        return Response({"message": "You sent no options to update"},status=status.HTTP_400_BAD_REQUEST)
     category = get_object_or_404(Categories, id= category_id)
     serialized = CategoriesSerializer(category, request.data, partial=True)
     if serialized.is_valid():
        serialized.save()

     return Response(serialized.data,status=status.HTTP_200_OK)



class CategoriesView(APIView):
  #  authentication_classes = [TokenAuthentication]
  #  permission_classes = [IsSuperuserAllowGetForAll]
   def get(self, request):
    categories = Categories.objects.all()
    serialized =  CategoriesSerializer(categories, many=True)
    return Response(serialized.data,status=status.HTTP_200_OK)
  
   def delete(self, request):
     categories = Categories.objects.all()
     categories.delete()
     return Response({"Message":f"Deleted all categories"},status=status.HTTP_200_OK)