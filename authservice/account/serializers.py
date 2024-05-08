from django.utils.encoding import force_str
from rest_framework import serializers
from .models import UserData
import requests


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        print(validated_data)
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()

        # Send email
        self.send_email(validated_data['email'], validated_data['name'])
        
        return user

    def send_email(self, email, name):
        # Set up the data for the POST request
        email_data = {
            "from_email": "todo-app-admin@todoapp.com",
            "to_email": email,
            "subject": "Welcome to our service!",
            "message": "Hi {}, thank you for registering.".format(name)
        }
        # URL of the external service to send email
        url = 'http://127.0.0.1:8001/send-email/'
        try:
            response = requests.post(url, json=email_data)
            response.raise_for_status()
        except requests.RequestException as e:
            # Handle error, log it, etc.
            print(f"Failed to send email: {str(e)}")
