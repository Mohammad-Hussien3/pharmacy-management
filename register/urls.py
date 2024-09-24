from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.LogIn.as_view(), name='logIn'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='refreshCustomToken'),
    path('allusers/', views.AllUsers.as_view(), name='getAllUsers'),
    path('logout/<int:id>/', views.LogOut().as_view(), name='logOut'),
]