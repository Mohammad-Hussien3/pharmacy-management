from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='refresh_custom_token'),
    path('allusers/', views.AllUsers.as_view()),
]