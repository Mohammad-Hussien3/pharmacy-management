from django.urls import path
from . import views

urlpatterns = [
    path('allproducts/', views.AllProducts.as_view(), name='getAllProducts'),
    path('addproduct/', views.AddProduct.as_view(), name='AddProduct'),
    path('editquantity/<int:id>/<int:number>/', views.EditQuntity.as_view(), name='changeTheQuantity'),
    path('editprice/<int:id>/', views.EditPrice.as_view(), name='changeThePrice'),
]