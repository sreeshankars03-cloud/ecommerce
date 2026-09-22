
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

# Generate JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


# Register API
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response({
                'user': {
                    'username': user.username,
                    'role': user.role
                },
                'token': tokens
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens_for_user(user)

            return Response({
                'user': {
                    'username': user.username,
                    'role': user.role
                },
                'token': tokens
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#test API
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsMerchant, IsCustomer

class TestProtectedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "You are Authenticated."})

   