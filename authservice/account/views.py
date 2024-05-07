from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, get_user_model
from django.utils.crypto import get_random_string
import requests
from rest_framework.views import APIView

from .models import UserData
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated

# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class IsAuthenticatedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'is_authenticated': True})

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if isinstance(user, AnonymousUser):
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(request.data.get('old_password')):
            return Response({'detail': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({'detail': 'Password changed successfully'})

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(UserData, email=email)
        new_password = get_random_string(8)  # Generate a new random password
        user.set_password(new_password)
        user.save()
        self.send_email(user, 'Password Reset',f'Your new password is: {new_password}','admin@example.com')
        return Response({'detail': 'New password has been sent to your email'})

    def send_email(self, user, subject, message, from_address):
        # Set up the data for the POST request
        # "to_email": user.email,
        email_data = {
            "to_email": user.email,
            "from_email": "balamurugan.sekar@gmail.com",
            "subject": subject,
            "message": message
        }
        # URL of the external service to send email
        url = 'http://127.0.0.1:8001/send-email/'
        try:
            response = requests.post(url, json=email_data)
            response.raise_for_status()
        except requests.RequestException as e:
            # Handle error, log it, etc.
            print(f"Failed to send email: {str(e)}")

class PasswordResetView(APIView):
    def post(self, request):
        user = get_user_model().objects.get(email=request.data.get('email'))
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({'detail': 'Password reset successful'})