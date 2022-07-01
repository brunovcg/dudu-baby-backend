from django.urls import path
from .views import CategoriesView,CategoriesOneView

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:category_id>/', CategoriesOneView.as_view())
]
