from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
import json
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .tokens import CustomToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# Create your views here.

def check_keys(expected_keys, received_keys):
    return received_keys == expected_keys


def error_keys(expected_keys, received_keys):
    return JsonResponse(
                {'error': 'Invalid keys in the request data.', 'expected': list(expected_keys), 'received': list(received_keys)},
                status=status.HTTP_400_BAD_REQUEST
            )


class Register(APIView):
    
    expected_keys = {'email', 'password', 'username'}
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'success'}, status=status.HTTP_201_CREATED)
        
        return JsonResponse({'message':'failed'}, status=status.HTTP_400_BAD_REQUEST)
    

class LogIn(APIView):

    expected_keys = {'username', 'password'}
    permission_classes = [AllowAny]
    
    def put(self, request):
        data = json.loads(request.body.decode('utf-8'))
        received_keys = set(data.keys())
        if not check_keys(self.expected_keys, received_keys):
            error_keys(self.expected_keys, received_keys)
        
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = CustomToken.for_user(user)
            return JsonResponse({'token': str(token.access_token), 'refresh': str(token)}, status=status.HTTP_202_ACCEPTED)
        
        return JsonResponse({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
