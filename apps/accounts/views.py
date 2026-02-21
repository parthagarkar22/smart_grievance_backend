


from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
    
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    """
    Citizen registration
    Default role = CITIZEN
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "role": user.role,
                    "department": user.department,
                }
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "department": user.department,
                }
            },
            status=status.HTTP_200_OK
        )



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)

            return Response(
                {
                    "access_token": new_access
                },
                status=status.HTTP_200_OK
            )

        except TokenError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
