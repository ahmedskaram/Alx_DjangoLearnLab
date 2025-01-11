from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

# Using get_user_model to dynamically fetch the user model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Using serializers.CharField to define the password field as write-only
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'followers']

    def create(self, validated_data):
        # Explicitly using get_user_model().objects.create_user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create a token for the user
        Token.objects.create(user=user)
        return user
