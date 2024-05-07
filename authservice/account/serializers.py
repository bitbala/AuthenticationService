from rest_framework import serializers
from .models import UserData
import requests


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()

        # Send email
        self.send_email(user)
        
        return user

    def send_email(self, user):
        # Set up the data for the POST request
        email_data = {
            "email": user.email,
            "subject": "Welcome to our service!",
            "message": "Hi {}, thank you for registering.".format(user.name)
        }
        # URL of the external service to send email
        url = 'http://127.0.0.1:8001/send-email/'
        try:
            response = requests.post(url, json=email_data)
            response.raise_for_status()
        except requests.RequestException as e:
            # Handle error, log it, etc.
            print(f"Failed to send email: {str(e)}")
