from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    # Explicitly define password as a CharField
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # Use get_user_model for flexibility
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'followers']

    def create(self, validated_data):
        # Use get_user_model().objects.create_user for user creation
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create a token for the user
        Token.objects.create(user=user)
        return user
