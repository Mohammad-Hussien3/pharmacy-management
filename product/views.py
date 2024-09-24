from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
import json
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

class AllProducts(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        jsonProducts = [ProductSerializer(product) for product in products]
        return JsonResponse(jsonProducts, safe=False, status=status.HTTP_202_ACCEPTED)