from django.urls import path
from . import views

urlpatterns = [
    path('allproducts/', views.AllProducts.as_view(), name='getAllProducts'),
]