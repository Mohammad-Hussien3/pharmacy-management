from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
import json
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Product
from .serializers import ProductSerializer
# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


def error_keys(expected_keys, received_keys):
    return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AllProducts(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        jsonProducts = [ProductSerializer(product).data for product in products]
        return JsonResponse(jsonProducts, safe=False, status=status.HTTP_202_ACCEPTED)
    
class AddProduct(APIView):

    permission_classes = [IsAdminUser]
    expected_keys = {'name', 'price', 'quantity', 'description'}

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)

        newProduct = ProductSerializer(data=data)
        if newProduct.is_valid():
            newProduct.save()
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        
        return JsonResponse({'message':'failed'}, status=status.HTTP_401_UNAUTHORIZED)

class EditQuntity(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, id, number):
        product = Product.objects.get(id=id)
        product.quantity += number * 2 - 1
        product.save()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)
    
class EditPrice(APIView):

    expected_keys = {'newPrice'}
    permission_classes = [IsAdminUser]

    def post(self, request, id):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)

        product = Product.objects.get(id=id)
        newPrice = data.get('newPrice')
        product.price = newPrice
        product.save()
        return JsonResponse({'message':'success'}, status=status.HTTP_200_OK)