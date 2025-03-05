from rest_framework import generics, permissions
from .models import PasswordEntry
from .serializers import PasswordEntrySerializer
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# from django.shortcuts import redirect
# from django.urls import reverse

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # First create the user
        response = super().create(request, *args, **kwargs)
        
        # Now log the user in by generating a JWT token
        user = User.objects.get(username=request.data['username'])
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Add tokens to the response data (you can return this to the frontend)
        response_data = response.data
        response_data['access'] = access_token
        response_data['refresh'] = refresh_token

        return Response(response_data, status=response.status_code)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Call the parent method to obtain the tokens
        response = super().post(request, *args, **kwargs)

        # If login is successful, include the tokens in the response
        if response.status_code == 200:
            # You can retrieve tokens from the response
            access_token = response.data['access']
            refresh_token = response.data['refresh']

            # Include the tokens in the response data
            response_data = {
                'access': access_token,
                'refresh': refresh_token,
            }

            return Response(response_data, status=response.status_code)

        return response

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
            
            RefreshToken(refresh_token).blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        

class PasswordEntryListCreate(generics.ListCreateAPIView):
    serializer_class = PasswordEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class PasswordEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PasswordEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)