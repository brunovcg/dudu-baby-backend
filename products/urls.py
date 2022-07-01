from django.urls import path
from .views import ProductsView, ProductOneView, MassiveLoadView

urlpatterns = [
    path('products/', ProductsView.as_view()),
    path('products/<int:product_id>/', ProductOneView.as_view()),
    path('products/massiveload/', MassiveLoadView.as_view())
]
